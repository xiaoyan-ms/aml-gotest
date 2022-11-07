#################

FROM mcr.microsoft.com/oss/go/microsoft/golang:1.18 

RUN mkdir /build
COPY . /build/
WORKDIR /build

RUN go get -v -d ./...
RUN go build src/*.go

ENTRYPOINT ["./main"]
CMD []
