#!/usr/bin/env Rscript

cols <- function(y){
   cat("This function will print sum of the column whose index is passed from commandline\n")
   cat("processing...column sums\n")
   su<-sum(data[,y])
   cat(su)
   cat("\n")
}

rows <- function(y){
   cat("This function will print sum of the row whose index is passed from commandline\n")
   cat("processing...row sums\n")
   su<-sum(data[y,])
   cat(su)
   cat("\n")
}
#calling a function based on its name from commandline … y is the row or column index
FUN <- function(run_func,y){
    switch(run_func,
        rows=rows(as.numeric(y)),
        cols=cols(as.numeric(y)),
        stop("Enter something that switches me!")
    )
}

args <- commandArgs(TRUE)
cat("you passed the following at the command line\n")
cat(args);cat("\n")
filename<-args[1]
func_name<-args[2]
attr_index<-args[3]
data<-read.csv(filename,header=T)
cat("Matrix is:\n")
print(data)
cat("Dimensions of the matrix are\n")
cat(dim(data))
cat("\n")
FUN(func_name,attr_index)
