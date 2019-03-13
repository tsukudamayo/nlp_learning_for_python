package main

import (
    "fmt"
    "log"
    "os/exec"
)

func main() {
    out, err := exec.Command("C:/Users/tsukuda/tools/Miniconda3/envs/jpnlp32/python.exe ontology_filter.py").Output()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("command exec %s", out)
}
