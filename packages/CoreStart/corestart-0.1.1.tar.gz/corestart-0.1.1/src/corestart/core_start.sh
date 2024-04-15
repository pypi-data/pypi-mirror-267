#!/bin/bash

# 프로젝트의 폴더 구조 생성
mkdir -p api streamlit models database scripts tests docs notebooks logs data docker

# 각 폴더에 README.md 파일 추가
for dir in api streamlit models database scripts tests docs notebooks logs docker
do
    echo "This directory is for $(echo $dir | sed 's/\/$//')" > $dir/README.md
done

echo "폴더 구조 및 README 파일이 생성되었습니다."

