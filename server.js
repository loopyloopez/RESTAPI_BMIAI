
const PORT = 3000 
import express from "express"
import { exec } from "child_process"
const App = express()

const URL = "localhost:3000/API?prom=hi"



App.get("/API",(req,res)=>{
    //console.log(req.query.prom)
    let Name = req.query.prom
    exec(`python ./PyStuff/main.py ${Name}`,(error,stdout,stderr)=>{
        console.log(`printed results were: ${stdout}`)
        const outputString = stdout.toString().trim()
        res.send(outputString)
    })
})



App.listen(3000,"0.0.0.0",()=>{
    console.log(`Server is running on port ${PORT}`)
})