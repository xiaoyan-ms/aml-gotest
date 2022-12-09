## Azure resource
[pytest-endpoint3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/c830bb7a-83f5-45e3-81fc-3c2053e7d16f/resourceGroups/xiaoyan-group-dev/providers/Microsoft.MachineLearningServices/workspaces/xiaoyan-aml-ws/onlineEndpoints/pytest-endpoint4/overview)


## Commands to build & deploy

az login  
az account set --subscription c830bb7a-83f5-45e3-81fc-3c2053e7d16f  
az acr login --name xiaoyanacr  

docker build . -f Dockerfile -t xiaoyanacr.azurecr.io/test/aml-pytest:1209-2
docker run -p 8000:8000  xiaoyanacr.azurecr.io/test/aml-pytest:1209-1
docker push  xiaoyanacr.azurecr.io/test/aml-pytest:1209-1

docker build . -f Dockerfile3 -t xiaoyanacr.azurecr.io/test/gpu-test:1209-1
docker push  xiaoyanacr.azurecr.io/test/gpu-test:1209-1

az ml online-endpoint create  -f pytest-endpoint.yml --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws  
az ml online-deployment create  -f pytest-deployment.yml --all-traffic --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws  

az ml online-endpoint get-credentials --name pytest-endpoint1  --resource-group xiaoyan-group-dev --workspace-name xiaoyan-aml-ws

az deployment group create --mode incremental \
    --resource-group cm-mop-prod-eastus \
    --template-file 1b-deploy-deployment.json \
    --parameters \
        annotationEhName= \
        datastore=workspaceblobstore \
        ehNamespace= \
        environment=prod \
        includeCode=True \
        includeInferenceConfig=False \
        instanceCount=1 \
        livenessPath= \
        livenessPort=0 \
        maxConcurrentRequestsPerInstance=100 \
        readinessPath= \
        readinessPort=0 \
        mirrorTrafficTargetEndpoint= \
        scoringPath= \
        scoringPort=0 \
        sqlDatabase= \
        sqlServer= \
        structuredEventEhName= \
        auxStructuredEventEhName= \
        unstructuredEventEhName= \
        auxUnstructuredEventEhName= \
        workQueueEhName= \
        globalResourceGroup=xiaoyan-group-dev \
        globalUserAssignedIdentity=xiaoyan-mi \
        scoringScript=score.py \
        version=1 \
        condaFileContents=@conda-env.yml \
        codeDirRelPath=XiaoyanTest/GpuTest/1/code \
        modelDirRelPath=XiaoyanTest/GpuTest/1/model \
        deployment=xiaoyan-gputest-v1 \
        endpoint=xiaoyan-gputest \
        imageUri=xiaoyanacr.azurecr.io/test/gpu-test:1209-1 \
        instanceType=Standard_DS2_v2 \
        name=xiaoyan-gputest \
        workspace=xiaoyan-aml-ws \



## Deploy to MOP GPU instance

az account set --subscription c920e969-c175-44e3-a64b-d3009bafe279

docker build . -f Dockerfile2 -t xiaoyanacr.azurecr.io/test/aml-pygputest:1209-1
docker push  xiaoyanacr.azurecr.io/test/aml-pygputest:1209-1

az ml online-endpoint create  -f pygputest-endpoint.yml --resource-group cm-mop-prod-eastus --workspace-name cm-mop-aml-eastus
az ml online-deployment create  -f pygputest-deployment.yml --all-traffic --resource-group cm-mop-prod-eastus --workspace-name cm-mop-aml-eastus


az deployment group create --mode incremental \
    --resource-group cm-mop-prod-eastus \
    --template-file 1b-deploy-deployment.json \
    --parameters \
        annotationEhName= \
        datastore=workspaceblobstore \
        ehNamespace= \
        environment=prod \
        includeCode=True \
        includeInferenceConfig=False \
        instanceCount=1 \
        livenessPath= \
        livenessPort=0 \
        maxConcurrentRequestsPerInstance=100 \
        readinessPath= \
        readinessPort=0 \
        mirrorTrafficTargetEndpoint= \
        scoringPath= \
        scoringPort=0 \
        sqlDatabase= \
        sqlServer= \
        structuredEventEhName= \
        auxStructuredEventEhName= \
        unstructuredEventEhName= \
        auxUnstructuredEventEhName= \
        workQueueEhName= \
        
        globalResourceGroup=raiglobalprod \
        globalUserAssignedIdentity=raiuai \
        scoringScript=aml_score.py \
        version=14 \

        condaFileContents=@/tmp/tmpswu2ap7d \
        codeDirRelPath=RemoteUpload/CodeVulnerability/14/code \
        modelDirRelPath=RemoteUpload/CodeVulnerability/14/model \
        deployment=rai-codevulnerability-prod-v14 \
        endpoint=rai-codevulnerability-prod \
        imageUri=raiglobalprodacr.azurecr.io/openmpi4.1.0-cuda11.1-cudnn8-ubuntu20.04:40t3 \
        instanceType=Standard_NC6s_v3 \
        name=CodeVulnerability \
        workspace=cm-mop-aml-eastus \