# Translate App

*This app has been created as an homework for the interview process. 
The purpose of sharing this out is to present my current skills for the recruiters and future processes.* 

## Techs Used

- **Python 3.12**
- [**FastAPI**](https://fastapi.tiangolo.com/) - A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- [**Pytest**](https://docs.pytest.org/en/stable/) - A framework that makes building simple and scalable test cases easy.
- [**PyTorch**](https://pytorch.org/) Fully featured framework for building deep learning models.
- [**Swagger**](https://swagger.io/) - Auto-generated API documentation via OpenAPI, available at `/docs`.

## Setup

### Docker

Make sure you have Docker installed on your machine.

1. Inside the **root** directory, run the following command to build the Docker image:

   `docker build -t translate-app .`

2. Once the build is successful, run the container with the following command:

   `docker run -p 8000:8000 translate-app`
3. Access the app at http://0.0.0.0:8000/, where you should see the API's base response.
4. For API documentation (Swagger UI), visit: http://0.0.0.0:8000/docs

### Manual Setup (Without Docker)
If you prefer not to use Docker, follow the manual steps to set up the project locally:

1. Make sure you have Python 3.12 installed on your machine.

2. Install Poetry if it's not already installed:

    `curl -sSL https://install.python-poetry.org | python3 -`
3. Set up the virtual environment and install dependencies:

    `poetry install`
4. Run the FastAPI app:

    `poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`
5. The app should now be accessible at http://localhost:8000/.

### Running Tests

To run the tests, use the following command:

`poetry run pytest api/tests/`


### Scaling the application (AWS Example)

- **Containerization with Docker and Amazon ECR**: 
  Dockerize the application and push the Docker image to **Amazon ECR** for easy management and deployment of the container.

- **Orchestration Options**:
  - **Amazon EKS**: A fully managed Kubernetes service, best for complex applications needing Kubernetes features like pod autoscaling and advanced orchestration.
  - **Amazon ECS**: A simpler container orchestration service, with **AWS Fargate** offering serverless containers, ideal for simpler applications.

### Deploying CI/CD

To streamline the deployment process, a Continuous Integration/Continuous Deployment (CI/CD) pipeline would automate the steps from code changes to deployment:

- **CI/CD Tools**: 
  Use tools like **Jenkins**, **GitLab CI**, **GitHub Actions**, or cloud-native solutions like **AWS CodePipeline**.

- **Automatic Builds and Deployments**: 
  When a developer pushes changes to the repository (e.g., GitHub), the CI/CD pipeline would automatically:
  - Build the Docker image.
  - Push it to the container registry.
  - Trigger a deployment to the Kubernetes cluster.
