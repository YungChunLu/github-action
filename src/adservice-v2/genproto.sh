#!/bin/bash -eu

#!/bin/bash -e

PATH=$PATH:$GOPATH/bin
protodir=../../pb

python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I $protodir $protodir/demo.proto