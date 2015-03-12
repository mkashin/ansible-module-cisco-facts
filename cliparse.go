package main

import (
  "fmt"
  "strings"
  "os"
  "encoding/json"
  "io/ioutil"
)

type textObj struct {
  Config string
	Text string
}

func printDevice(obj textObj ) {
  jsonDevice, _ := json.Marshal(obj)
  fmt.Println(string(jsonDevice))
}

func main()   {
  // create a device with default settings
  tObject := textObj{"running",""}
  // read ansible arguments supplied as a file
  data, err:= ioutil.ReadFile(os.Args[1])
  if err != nil { 
    panic(err) 
  }
  // split arguments into a slice
  args := strings.Split(string(data)," ")
  // iterate over arguments updating default device
  for _,arg := range args {
      kvp := strings.Split(arg,"=")
      switch kvp[0] {
      case "element":
        tObject.Config = kvp[1]
      case "text":
        tObject.Text = kvp[1]

      }
  }

  printDevice(tObject)
  os.Exit(0)

}