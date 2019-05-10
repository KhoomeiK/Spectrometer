#!/bin/bash

function finish {
  p=$(ps ax | grep "python -m flask run" | awk 'NR==1{print $1}')
  echo $p
  kill $p
}
trap finish EXIT

cd backend
python -m flask run &
cd ..
npm run start