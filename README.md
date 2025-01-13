# AIKube

AIKube is a mini-project that demonstrates deploying a FastAPI-based application, a machine learning model, and a PostgreSQL database within a Kubernetes cluster. The project also incorporates Docker and Kubernetes configuration for seamless DevOps integration.

---

## Features

- **FastAPI**:
  - RESTful API for text analysis.
  - Integrates with a machine learning model for sentiment analysis.
  - Stores results in a PostgreSQL database.
  
- **Machine Learning Model**:
  - Sentiment analysis using Hugging Face's transformers.
  - Deployed as a separate microservice.

- **PostgreSQL**:
  - Serves as the database backend for storing text and sentiment data.

- **Kubernetes Deployment**:
  - Kubernetes manifests for FastAPI, ML model, and PostgreSQL.
  - Configured with `NodePort` and `ClusterIP` services for internal and external communication.

---

## Architecture

The application consists of the following components:

1. **FastAPI App**:
   - Handles API requests for text analysis.
   - Communicates with the ML model service.

2. **ML Model**:
   - Provides sentiment analysis as a microservice.

3. **PostgreSQL**:
   - Stores text and sentiment results.

The application is containerised using Docker and orchestrated with Kubernetes.

```mermaid

flowchart LR
	n00(Ingress <br/> Controller)
	subgraph g20["Kubernetes Cluster"]
		subgraph h00[" "]
			subgraph g10["Docker Image"]
				n10["FastAPI <br/> (API Gateway)"]
				n20["SQLAlchemy"]
			end
			subgraph g11["Docker Image"]
				n30["PostgreSQL <br/> (Database)"]
			end
			subgraph g12["Docker Image"]
				n11["FastAPI <br/> (Internal)"]
				n40["ML Model <br/> Semantic Analysis"]
			end
		end	
	end

	n00 -- HTTP <br/> Requests ----> n10
	n10 <--> n20
	n20 <-- SQL <br/> Transactions --> n30
	n11 <--> n10
	n11 <--> n40

	classDef node0Style fill:#1697a6, stroke:#B4B4B4
	classDef node1Style fill:#ffb3ae, stroke:#B4B4B4
	classDef node2Style fill:#ffc24b, stroke:#B4B4B4
	classDef node3Style fill:#f47068, stroke:#B4B4B4
	classDef node4Style fill:#118ab2, stroke:#B4B4B4
	classDef hiddenStyle fill:transparent, stroke:transparent
	class n00,n01,n02,n03,n04,n05,n06,n07,n08,n09 node0Style;
	class n10,n11,n12,n13,n14,n15,n16,n17,n18,n19 node1Style;
	class n20,n21,n22,n23,n24,n25,n26,n27,n28,n29 node2Style;
	class n30,n31,n32,n33,n34,n35,n36,n37,n38,n39 node3Style;
	class n40,n41,n42,n43,n44,n45,n46,n47,n48,n49 node4Style;
	class h00,h01,h02,h03,h04,h05,h06,h07,h08,h09 hiddenStyle;
	
```

---

## Setup

### Prerequisites

- Docker Desktop with Kubernetes enabled.
- Kubernetes CLI (`kubectl`).
- A running Docker registry (local or remote).

---

### Steps to Run

1. **Clone the Repository**
```bash
git clone <repository-url>
cd aikube
```

2. **Build Docker Images**
```bash
docker build -t localhost:5002/aikube-fastapi_app:latest ./fastapi_app
docker build -t localhost:5002/aikube-ml_model:latest ./ml_model
 ```

3. **Push Images to Local Registry**
```bash
docker push localhost:5002/aikube-fastapi_app:latest
docker push localhost:5002/aikube-ml_model:latest
```

4. **Deploy to Kubernetes**
```bashApply all Kubernetes manifests:
kubectl apply -f kubernetes/
```

5. **Verify Deployment**
Check the status of all pods and services:
```bash
kubectl get pods
kubectl get services
 ```

6. **Access the Application**
Use the assigned NodePort to interact with the FastAPI app. For example:
```bash
curl -X POST http://localhost:<NodePort>/analyse_text \
-H "Content-Type: application/json" \
-d '{"text": "I love Kubernetes!"}'
File Structure
 ```
