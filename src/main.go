package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos"
)

func main() {
	fmt.Println("hello")

	startHttpServer(8000)
}

func startHttpServer(port int) {
	mux := http.NewServeMux()
	srv := &http.Server{
		Addr:    fmt.Sprintf("0.0.0.0:%d", port),
		Handler: mux,
	}

	mux.HandleFunc("/liveness", livenessController)
	mux.HandleFunc("/readiness", livenessController)
	mux.HandleFunc("/annotate", annotateController)

	srv.ListenAndServe()

}

func livenessController(wr http.ResponseWriter, req *http.Request) {
	wr.WriteHeader(http.StatusOK)
	wr.Write([]byte("OK"))
}

func annotateController(wr http.ResponseWriter, req *http.Request) {
	result, err := getItemsFromCosmos(
		"9fd61a68-1faa-4bca-9a4e-8611b254d342",
		"https://xiaoyan-cosmos-test.documents.azure.com:443/",
		"config", "policies", "policy")

	if err == nil {
		r, err := json.Marshal(result)
		if err == nil {
			wr.Header().Set("Content-Type", "application/json")
			wr.WriteHeader(http.StatusOK)
			wr.Write(r)
		}
	}
	wr.WriteHeader(http.StatusInternalServerError)
	wr.Write([]byte(fmt.Sprintf("error: %s", err)))
}

func getItemsFromCosmos(clientId string, endpoint string, dbName string, containerName string, pkValue string) ([]interface{}, error) {
	credential, err := GetMICredential(clientId)
	if err != nil {
		return nil, err
	}

	client, err := azcosmos.NewClient(endpoint, credential, nil)
	if err != nil {
		return nil, err
	}

	container, err := client.NewContainer(dbName, containerName)
	if err != nil {
		return nil, err
	}

	pk := azcosmos.NewPartitionKeyString(pkValue)
	queryPager := container.NewQueryItemsPager("select * from docs c", pk, nil)
	ctx := context.Background()
	result := make([]interface{}, 0)
	for queryPager.More() {
		page, err := queryPager.NextPage(ctx)
		if err != nil {
			return nil, err
		}
		for _, item := range page.Items {
			var p map[string]interface{}
			err := json.Unmarshal(item, &p)
			if err != nil {
				return nil, err
			}

			result = append(result, p)
		}
	}
	return result, nil
}

func GetMICredential(clientId string) (*azidentity.ManagedIdentityCredential, error) {
	var opts *azidentity.ManagedIdentityCredentialOptions
	if clientId == "" {
		opts = nil
	} else {
		id := azidentity.ClientID(clientId)
		opts = &azidentity.ManagedIdentityCredentialOptions{ID: id}
	}
	return azidentity.NewManagedIdentityCredential(opts)
}
