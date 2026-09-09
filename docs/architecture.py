from diagrams import Diagram, Cluster, Edge
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import StepFunctions
from diagrams.aws.compute import Lambda
from diagrams.onprem.database import Mongodb
from diagrams.custom import Custom

# Atributos de estilo globais para melhorar a estética
graph_attr = {
    "fontsize": "22",
    "fontcolor": "#2D3436",
    "pad": "1.0",
    "splines": "spline",
    "nodesep": "0.8",
    "ranksep": "1.5",
    "bgcolor": "white"
}

node_attr = {
    "fontcolor": "#2D3436"
}

edge_attr = {
    "color": "#636E72",
    "penwidth": "2.0"
}

with Diagram("Event-Driven Data Consolidation", show=False, direction="LR", 
             graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr):
    
    # Nó customizado do Floci
    floci = Custom("Floci AWS Emulator", "../floci/floci_logo.png")
    
    with Cluster("AWS Cloud (Local)", graph_attr={"bgcolor": "#F4F5F7", "pencolor": "#B3BAC5"}):
        
        with Cluster("Compute & Orchestration", graph_attr={"bgcolor": "#FFFFFF", "pencolor": "#FF9900"}):
            orchestrator = StepFunctions("Step Functions - Orchestrator")
            processor = Lambda("Lambda - Data Consolidation")
            
        with Cluster("Source Data (Microservices)", graph_attr={"bgcolor": "#E3F2FD", "pencolor": "#90CAF9"}):
            dynamo_profile = Dynamodb("DynamoDB - User Profiles")
            dynamo_activity = Dynamodb("DynamoDB - User Activity")
            sources = [dynamo_profile, dynamo_activity]

        dynamo_status = Dynamodb("DynamoDB - Execution Status")

    # Representando o banco externo (Atlas simulando o DocumentDB)
    app_db = Mongodb("MongoDB Atlas - App Database")

    # Fluxo Horizontal Principal (Com peso máximo)
    floci >> Edge(label="Trigger Event", color="#A0A0A0", weight="100") >> orchestrator
    orchestrator >> Edge(label="Process Data", weight="100") >> processor
    
    # O Lambda escreve no MongoDB
    processor >> Edge(label="Upsert", weight="100") >> app_db

    # Forçando as caixas de banco de dados a ficarem "abaixo" da linha principal 
    # usando setas invisíveis para estruturar o layout verticalmente
    orchestrator >> Edge(style="invis") >> dynamo_profile
    processor >> Edge(style="invis") >> dynamo_status

    # Fluxo de Dados visível, porém com constraint="false" para não entortar o layout principal
    processor >> Edge(label="Update Status", constraint="false") >> dynamo_status
    dynamo_profile >> Edge(dir="back", style="dashed", label="getItem", constraint="false") >> orchestrator
    dynamo_activity >> Edge(dir="back", style="dashed", label="getItem", constraint="false") >> orchestrator