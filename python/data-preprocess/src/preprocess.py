#!/usr/bin/env python

def get_review_data(in_file_name):
    data["App"] = data["App"].apply(lambda s: s.lower())
    app_names = data["App"].tolist()
    data["App"].to_csv("app_names.csv", encoding="utf-8", index=False)
