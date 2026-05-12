import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def create_dashboard(archive, shelves_df, BW, BH, BD):
    """
    Creates an interactive dashboard with a Pareto Front and a 3D visualization.
    """
    # 1. Prepare Pareto Data
    utils = []
    balances = []
    hover_text = []
    
    for i, sol in enumerate(archive):
        # Using the first and second objective from your fitness
        # Note: we negate balance back to positive for the plot
        from engine import evaluate
        u, b = evaluate(sol, shelves_df, BW, BH, BD)
        utils.append(u)
        balances.append(abs(b))
        hover_text.append(f"Solution {i}<br>Utilization: {u:.2%}<br>StdDev Load: {abs(b):.2f}")

    # 2. Create Layout
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.4, 0.6],
        specs=[[{"type": "scatter"}, {"type": "scene"}]],
        subplot_titles=("Pareto Front (Click a point!)", "3D Shelf View")
    )

    # 3. Add Pareto Scatter Plot
    fig.add_trace(
        go.Scatter(
            x=utils, y=balances,
            mode='markers',
            marker=dict(size=12, color=utils, colorscale='Viridis', showscale=False),
            text=hover_text,
            hoverinfo='text',
            name='Solutions'
        ),
        row=1, col=1
    )

    # 4. Add 3D Visualization for the BEST Solution (initial view)
    # We choose the solution with highest utilization by default
    best_idx = np.argmax(utils)
    fig = add_solution_to_fig(fig, archive[best_idx], shelves_df, BW, BH, BD)

    # 5. Dashboard Formatting
    fig.update_layout(
        title="NSGA-II Optimization Results",
        template="plotly_dark",
        scene=dict(
            xaxis=dict(range=[0, BW], title="Width"),
            yaxis=dict(range=[0, BD], title="Depth"), # Plotly Y is Depth
            zaxis=dict(range=[0, BH], title="Height"),
            aspectmode='manual',
            aspectratio=dict(x=1, y=BD/BW, z=BH/BW)
        ),
        clickmode='event+select'
    )

    fig.show()

def add_solution_to_fig(fig, solution, shelves_df, BW, BH, BD):
    """Adds cuboids for products and shelves to the Plotly scene."""
    
    # Add Shelves (Grey Plates)
    for i, s in shelves_df.iterrows():
        fig.add_trace(_make_cuboid(
            0, 0, s['pos'], BW, BD, s['thick'], 
            name=f"Shelf {i}", color='rgba(150, 150, 150, 0.5)', showlegend=False
        ), row=1, col=2)

    # Add Products
    for p in solution:
        name = f"Type: {p['product'].get('product_type', 'N/A')}"
        fig.add_trace(_make_cuboid(
            p['x'], p['z'], p['y'], # Mapping X, Z(Depth), Y(Height)
            p['eff_width'], p['eff_length'], p['eff_height'],
            name=name, color='rgba(255, 50, 50, 0.8)'
        ), row=1, col=2)
    
    return fig

def _make_cuboid(x, y, z, dx, dy, dz, name, color, showlegend=True):
    """Helper to create a 3D Meshbox for Plotly."""
    # 8 Vertices of a cube
    v_x = [x, x+dx, x+dx, x, x, x+dx, x+dx, x]
    v_y = [y, y, y+dy, y+dy, y, y, y+dy, y+dy]
    v_z = [z, z, z, z, z+dz, z+dz, z+dz, z+dz]
    
    return go.Mesh3d(
        x=v_x, y=v_y, z=v_z,
        # Define triangles to form the 6 faces
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color,
        opacity=0.8,
        name=name,
        hoverinfo="name",
        showlegend=showlegend
    )