import streamlit as st

# Gracefully handle the case where graphviz is not installed
try:
    import graphviz
    GRAPHVIZ_INSTALLED = True
except ImportError:
    GRAPHVIZ_INSTALLED = False

def display_graphviz_installation_instructions():
    """Displays a formatted, user-friendly message for installing Graphviz."""
    with st.container(border=True):
        st.error("🎨 Graph Visualization Disabled", icon="🎨")
        st.write("To enable the interactive graph visualizations, the `graphviz` library is required. Please follow the steps below:")
        st.markdown("""
            **Step 1: Install the Python Package**
            
            Open your terminal or command prompt and run this command:
        """)
        st.code("pip install graphviz streamlit", language="bash")
        st.markdown("""
            ---
            **Step 2: Install the Graphviz System Software**

            The Python package needs the underlying Graphviz software to function. You must install it for your operating system.
            
            ➡️ [**Click here to go to the official Graphviz download page**](https://graphviz.org/download/)
            
            *After installing, you may need to restart your terminal or computer. Then, restart the Streamlit app.*
        """)

def render_fuzzy_graph_theory():
    """Renders the educational section on Fuzzy Graph Theory."""
    st.header("1. Fuzzy Graph Theory: An Introduction")
    st.markdown("""
    A **fuzzy graph** is a powerful extension of a classical (or 'crisp') graph. In the real world, relationships and entities are often not black and white. A fuzzy graph allows us to model this uncertainty and ambiguity by representing connections and nodes with degrees of existence, rather than a simple 'yes' or 'no'.
    """)

    st.subheader("From Crisp to Fuzzy Sets")
    st.markdown("""
    To understand fuzzy graphs, you must first understand the journey from classical sets to fuzzy sets.
    - **Crisp Set:** In classical math, an item is either IN a set or OUT of it. There's no middle ground. For the set of "Even Numbers," 4 has a membership of 1 (it's in), and 3 has a membership of 0 (it's out).
    - **Fuzzy Set:** Proposed by Lotfi Zadeh in 1965, a fuzzy set allows for **partial membership**. An element can belong to a set to a certain degree, measured from 0 to 1.
    """)

    st.info("Interactive Demo: The Fuzzy Set of 'Tall People'")
    height = st.slider("Select a person's height (in cm):", 140, 220, 175)
    
    # Simple sigmoid-like function to determine membership in "tall"
    if height < 160:
        membership = 0.0
    elif height < 180:
        membership = (height - 160) / 20.0 * 0.8 # Scale up to 0.8
    elif height < 190:
        membership = 0.8 + ((height - 180) / 10.0 * 0.2) # Scale from 0.8 to 1.0
    else:
        membership = 1.0
    st.write(f"A person with a height of **{height} cm** has a membership value of **{membership:.2f}** in the fuzzy set of 'Tall People'.")
    st.progress(membership)

    st.subheader("Core Concepts of a Fuzzy Graph")
    st.markdown("""
    A fuzzy graph is formally defined as a pair $\\tilde{G} = (\\sigma, \\mu)$, consisting of a fuzzy vertex set and a fuzzy edge set.

    - **Fuzzy Vertex Set ($\\sigma$):** A function that assigns a membership value to each vertex. This value, $\\sigma(v)$, represents the degree to which the vertex *exists*. A value of 1 means it fully exists.
    - **Fuzzy Edge Set ($\\mu$):** A function that assigns a membership value to each edge. This value, $\\mu(u, v)$, represents the strength or degree of the relationship between two vertices.
    """)

    st.success("The Golden Rule of Fuzzy Graphs")
    st.markdown("The strength of an edge can never exceed the strength of the vertices it connects. This makes intuitive sense—a relationship can't be stronger than the entities it links.")
    st.latex(r"\mu(u, v) \le \min(\sigma(u), \sigma(v))")

    st.info("Interactive Demo: Build Your Own Fuzzy Graph!")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.write("Adjust Vertex & Edge Values:")
        sigma_a = st.slider("Vertex A Existence (σ)", 0.0, 1.0, 0.9, 0.05)
        sigma_b = st.slider("Vertex B Existence (σ)", 0.0, 1.0, 0.8, 0.05)
        sigma_c = st.slider("Vertex C Existence (σ)", 0.0, 1.0, 1.0, 0.05)
        mu_ab = st.slider("Edge A-B Strength (μ)", 0.0, 1.0, 0.7, 0.05)
        mu_bc = st.slider("Edge B-C Strength (μ)", 0.0, 1.0, 0.6, 0.05)
        mu_ac = st.slider("Edge A-C Strength (μ)", 0.0, 1.0, 0.5, 0.05)
    
    # Check the golden rule
    violations = []
    if mu_ab > min(sigma_a, sigma_b):
        violations.append(f"Edge A-B ({mu_ab:.2f}) is stronger than min(A, B) = {min(sigma_a, sigma_b):.2f}")
    if mu_bc > min(sigma_b, sigma_c):
        violations.append(f"Edge B-C ({mu_bc:.2f}) is stronger than min(B, C) = {min(sigma_b, sigma_c):.2f}")
    if mu_ac > min(sigma_a, sigma_c):
        violations.append(f"Edge A-C ({mu_ac:.2f}) is stronger than min(A, C) = {min(sigma_a, sigma_c):.2f}")

    with col2:
        st.write("Generated Fuzzy Graph:")
        if GRAPHVIZ_INSTALLED:
            # Create Graphviz graph
            dot = graphviz.Graph()
            dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', fontcolor='black')
            dot.attr('edge', fontcolor='darkgreen')
            dot.node('A', f"A (σ={sigma_a:.2f})")
            dot.node('B', f"B (σ={sigma_b:.2f})")
            dot.node('C', f"C (σ={sigma_c:.2f})")
            dot.edge('A', 'B', label=f"μ={mu_ab:.2f}")
            dot.edge('B', 'C', label=f"μ={mu_bc:.2f}")
            dot.edge('A', 'C', label=f"μ={mu_ac:.2f}")
            st.graphviz_chart(dot)
            if violations:
                for v in violations:
                    st.warning(f"Rule Violation: {v}")
            else:
                st.success("This is a valid fuzzy graph!")
        else:
            display_graphviz_installation_instructions()

    st.subheader("Key Terminology and Operations")
    with st.expander("Path, Strength, and Connectivity"):
        st.markdown("""
        - **Path:** A sequence of vertices where the connection strength between each step is greater than 0.
        - **Strength of a Path:** The "weakest link" in the chain. It is the *minimum* membership value of all edges in that path.
        - **Strength of Connectedness:** The strongest possible path between two vertices. It is the *maximum* strength over all possible paths between them.
        """)
    with st.expander("Order, Size, and Subgraphs"):
        st.markdown("""
        - **Order:** The sum of all vertex membership values.
        - **Size:** The sum of all edge membership values.
        - **Fuzzy Subgraph:** A fuzzy graph within another, where all its vertex and edge values are less than or equal to the corresponding values in the original graph.
        """)

    st.subheader("Types of Fuzzy Graphs")
    tab1, tab2, tab3 = st.tabs(["Complete Fuzzy Graph", "Fuzzy Tree", "Bipolar Fuzzy Graph"])
    with tab1:
        st.markdown("A fuzzy graph is **complete** if the strength of the edge between any two vertices is the maximum possible value it can take: $\\mu(u, v) = \\min(\\sigma(u), \\sigma(v))$. Every vertex is as connected as it can possibly be.")
    with tab2:
        st.markdown("A **fuzzy tree** is a fuzzy graph that contains no cycles, and for any two vertices, the path between them has the strongest possible connection strength.")
    with tab3:
        st.markdown("A **bipolar fuzzy graph** is an extension where edge values can range from -1 to 1. Positive values indicate connection/agreement, while negative values indicate repulsion/disagreement, modeling more complex relationships.")
    
    st.subheader("Applications of Fuzzy Graph Theory 🗺️")
    st.markdown("""
    -  socials **Social Network Analysis:** Modeling friendships or influence with varying degrees of strength.
    - decision **Decision Making:** Finding the most reliable (not necessarily shortest) path in a network, like transportation or data routing.
    - image **Image Processing:** Representing fuzzy relationships between pixels or regions in an image based on color or texture.
    - database **Database & Information Retrieval:** Clustering similar documents or objects based on fuzzy, non-binary relationships.
    - bio **Chemistry and Biology:** Modeling interactions between proteins or chemical compounds where bond strengths can vary.
    """)

def render_research_paper_summary():
    """Renders the summary of the Picture Fuzzy Sets research paper."""
    st.header("2. Picture Fuzzy Similarity Measures (Research Paper Deep Dive)")
    st.markdown("""
    This section breaks down the 2021 research paper by Surender Singh and Abdul Haseeb Ganie. The paper's goal is to fix critical flaws in how we measure similarity in **Picture Fuzzy Sets (PFS)** and apply these new, improved methods to real-world problems.
    """)

    st.error("""
    **The Core Problem:** Existing methods for comparing Picture Fuzzy Sets are often unreliable. When comparing two objects that are *very similar but not identical*, many old formulas incorrectly calculate the similarity as **1.0000**, treating them as a perfect match. This is a major issue where small differences are critical.
    """)

    st.subheader("The Evolution of Fuzzy Sets: An Interactive Analogy")
    st.markdown("To understand the paper, we must understand why Picture Fuzzy Sets are so powerful. Let's use an interactive voting analogy.")

    tab_fs, tab_ifs, tab_pfs = st.tabs(["Fuzzy Set (FS)", "Intuitionistic Fuzzy Set (IFS)", "Picture Fuzzy Set (PFS)"])

    with tab_fs:
        st.markdown("**Fuzzy Set (FS):** Handles one dimension: membership (e.g., support).")
        support_fs = st.slider("Degree of Support (Yes)", 0.0, 1.0, 0.7, key="fs")
        st.write(f"In this model, your opinion is simply a **{support_fs:.2f}** level of support.")

    with tab_ifs:
        st.markdown("**Intuitionistic Fuzzy Set (IFS):** Adds a second dimension: non-membership (e.g., opposition). The leftover is 'hesitation'.")
        support_ifs = st.slider("Degree of Support (Yes)", 0.0, 1.0, 0.6, key="ifs_s")
        oppose_ifs_max = 1.0 - support_ifs
        oppose_ifs = st.slider("Degree of Opposition (No)", 0.0, oppose_ifs_max, 0.2, key="ifs_o")
        hesitation = 1.0 - support_ifs - oppose_ifs
        st.write(f"Support (Yes): **{support_ifs:.2f}**")
        st.write(f"Opposition (No): **{oppose_ifs:.2f}**")
        st.info(f"Degree of Hesitation/Uncertainty: **{hesitation:.2f}**")

    with tab_pfs:
        st.markdown("""
        **Picture Fuzzy Set (PFS):** The most expressive model. It adds a third dimension: neutrality (abstention). The leftover is 'refusal'. This is the focus of the paper.
        """)
        support_pfs = st.slider("Degree of Support (Yes)", 0.0, 1.0, 0.5, key="pfs_s")
        oppose_pfs_max = 1.0 - support_pfs
        oppose_pfs = st.slider("Degree of Opposition (No)", 0.0, oppose_pfs_max, 0.2, key="pfs_o")
        abstain_pfs_max = 1.0 - support_pfs - oppose_pfs
        abstain_pfs = st.slider("Degree of Abstention (Neutral)", 0.0, abstain_pfs_max, 0.1, key="pfs_a")
        refusal = 1.0 - support_pfs - oppose_pfs - abstain_pfs
        st.write(f"Support (Yes): **{support_pfs:.2f}**")
        st.write(f"Opposition (No): **{oppose_pfs:.2f}**")
        st.write(f"Abstention (Neutral): **{abstain_pfs:.2f}**")
        st.info(f"Degree of Refusal to Participate: **{refusal:.2f}**")

    st.subheader("The Paper's Main Contributions 🏆")
    st.success("""
    The authors made four key contributions:
    1.  **Proposed Four New Similarity Measures ($S_1, S_2, S_3, S_4$):** These new formulas are specifically designed to be more precise and avoid the "false positive" issue of older methods.
    2.  **Applied them to Pattern Recognition:** Demonstrated their superiority using real-world data (the Iris plant dataset).
    3.  **Introduced the PFMST Clustering Algorithm:** A simpler, more efficient graph-based method for clustering data in a PFS environment.
    4.  **Created a New Attribute Weighting Formula:** A reliable way to determine the importance of criteria in multi-attribute decision-making (MADM) problems.
    """)

    st.subheader("Applications Deep Dive")
    app_tab1, app_tab2, app_tab3 = st.tabs(["📊 Pattern Recognition", "🕸️ Clustering Analysis", "⚙️ MADM"])

    with app_tab1:
        st.markdown("""
        **Goal:** To identify an unknown pattern by finding its best match from a set of known patterns.
        
        The paper showed that when faced with very similar but non-identical patterns, their new measures correctly identified the true best match, while older measures often failed or gave ambiguous results. They used a performance index called **Degree of Confidence (DoC)** on the Iris flower dataset, where their new measures achieved a higher DoC, proving their effectiveness.
        """)

    with app_tab2:
        st.markdown("""
        **Goal:** To group objects into clusters where items in the same cluster are highly similar.
        
        The paper introduces the **Picture Fuzzy Maximum Spanning Tree (PFMST)** algorithm. This method is simpler and computationally cheaper than previous techniques.
        """)
        st.info("Interactive Demo: PFMST Clustering Concept")
        st.markdown("Imagine we have 10 cars and their similarity scores. The algorithm builds the strongest possible 'skeleton' connecting all cars (the MST). We can then form clusters by 'cutting' the weakest links.")
        
        threshold = st.slider("Set Similarity Threshold (α)", 0.5, 0.9, 0.65, 0.01)
        
        st.write(f"By cutting all connections weaker than **{threshold:.2f}**, the cars separate into distinct clusters.")

        if GRAPHVIZ_INSTALLED:
            # Simplified MST from the paper's car example
            mst_dot = graphviz.Graph(comment='Maximum Spanning Tree')
            mst_dot.attr('node', shape='circle', style='filled', fillcolor='lightcoral')
            
            edges = {
                ('G9', 'G4'): 0.87, ('G7', 'G2'): 0.83, ('G6', 'G1'): 0.82,
                ('G7', 'G3'): 0.81, ('G7', 'G8'): 0.74, ('G10', 'G5'): 0.76,
                ('G3', 'G9'): 0.64, ('G8', 'G10'): 0.69, ('G1', 'G4'): 0.64,
            }

            for (u, v), weight in edges.items():
                if weight >= threshold:
                    mst_dot.edge(u, v, label=f"{weight:.2f}")
                else:
                    # To show they exist but are cut, we ensure the nodes are still present
                    mst_dot.node(u)
                    mst_dot.node(v)

            st.graphviz_chart(mst_dot)
        else:
            display_graphviz_installation_instructions()


    with app_tab3:
        st.markdown("""
        **Goal:** To select the best option from alternatives based on multiple criteria (e.g., choosing a supplier based on price, quality, and environmental impact).
        
        A key challenge is determining the **weight** (importance) of each criterion. The paper shows that standard methods can fail by giving identical weights to different attributes.
        
        Their proposed solution uses the new similarity measures to compare each attribute's performance against a theoretical "ideal solution," resulting in more logical and distinct weights. This leads to more reliable and robust decision-making.
        """)

# --- Main App ---
st.set_page_config(page_title="Fuzzy Concepts Explorer", layout="wide")

st.title("Interactive Guide to Fuzzy Graph Theory & Picture Fuzzy Sets")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Fuzzy Graph Theory", "Picture Fuzzy Similarity Measures (Research Paper)"])

if selection == "Fuzzy Graph Theory":
    render_fuzzy_graph_theory()
else:
    render_research_paper_summary()

