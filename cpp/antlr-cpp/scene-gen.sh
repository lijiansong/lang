#!/bin/bash

## Use ANTLR to generate the parser with visitor mode.

antlr4 -Dlanguage=Cpp -no-listener -visitor -o scene-runtime Scene.g4
