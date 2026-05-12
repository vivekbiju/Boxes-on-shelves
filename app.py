import streamlit as st
import random
import plotly.graph_objects as go
from models import load_data, generate_initial_population
from engine import evaluate, fast_non_dominated_sort, mutate, crossover

# UI Configuration
st.set_page_config(page_title="Shelf Optimizer", layout="wide")

st.sidebar.header("Evolution Parameters")
POP_SIZE = st.sidebar.slider("Population Size", 10, 100, 50)
GENS = st.sidebar.slider("Generations", 5, 100, 20)
MUT_RATE = st.sidebar.slider("Mutation Rate", 0.01, 0.5, 0.1)

st.title("📦 NSGA-II Shelf Packing Dashboard")

# Data Loading
try:
    products, bay, shelves = load_data('data/products.txt', 'data/baytp1.txt', 'data/shelves.txt')
    BW, BH, BD = bay['w'], bay['h'], bay['d']
    st.sidebar.success("Data Loaded")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if st.button("🚀 Run Optimization"):
    with st.spinner("Calculating optimal placements..."):
        pop = generate_initial_population(POP_SIZE, products, shelves, BW, BH, BD)
        progress = st.progress(0)
        
        for g in range(GENS):
            fits = [evaluate(s, shelves, BW, BH, BD) for s in pop]
            offspring = []
            for _ in range(POP_SIZE // 2):
                p1, p2 = random.sample(pop, 2)
                c1, c2 = crossover(p1, p2)
                offspring.extend([mutate(c1, MUT_RATE, shelves, BW, BH, BD), 
                                  mutate(c2, MUT_RATE, shelves, BW, BH, BD)])
            
            combined = pop + offspring
            comb_fits = [evaluate(s, shelves, BW, BH, BD) for s in combined]
            fronts = fast_non_dominated_sort(combined, comb_fits)
            
            # Survival of the fittest (NSGA-II selection)
            pop = []
            for f in fronts:
                if len(pop) + len(f) <= POP_SIZE: pop.extend([combined[i] for i in f])
                else: pop.extend([combined[i] for i in f[:POP_SIZE-len(pop)]]); break
            
            progress.progress((g + 1) / GENS)
        
        st.session_state['archive'] = [combined[i] for i in fronts[0]]

# Results Visualization
if 'archive' in st.session_state:
    archive = st.session_state['archive']
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Pareto Front")
        utils, balances = zip(*[evaluate(s, shelves, BW, BH, BD) for s in archive])
        fig_p = go.Figure(go.Scatter(x=utils, y=[-b for b in balances], mode='markers', 
                                    marker=dict(size=12, color='red', line=dict(width=1, color='black'))))
        fig_p.update_layout(xaxis_title="Space Utilization", yaxis_title="Load Imbalance (StdDev)")
        st.plotly_chart(fig_p, use_container_width=True)
        sel_idx = st.selectbox("Select Solution to View", range(len(archive)))

    with col2:
        st.subheader(f"3D Visualization (Solution {sel_idx})")
        fig_3d = go.Figure()
        # Draw Shelves
        for i, s in shelves.iterrows():
            fig_3d.add_trace(go.Mesh3d(x=[0, BW, BW, 0, 0, BW, BW, 0], y=[0, 0, BD, BD, 0, 0, BD, BD], 
                                     z=[s['pos'], s['pos'], s['pos'], s['pos'], s['pos']+s['thick'], s['pos']+s['thick'], s['pos']+s['thick'], s['pos']+s['thick']],
                                     color='gray', opacity=0.2, flatshading=True))
        # Draw Boxes
        for p in archive[sel_idx]:
            x, y, z, dx, dy, dz = p['x'], p['z'], p['y'], p['eff_width'], p['eff_length'], p['eff_height']
            fig_3d.add_trace(go.Mesh3d(x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x], y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy], 
                                     z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz], color='red', opacity=0.8))
        fig_3d.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig_3d, use_container_width=True)