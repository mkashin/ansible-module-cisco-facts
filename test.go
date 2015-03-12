package main

import (
  "fmt"
  "strings"
  "os"
  "encoding/json"
  "io/ioutil"
)

type remote_device struct {
  IP string
	Username string
	Password string
	Transport string
}

func printDevice(dev remote_device ) {
  jsonDevice, _ := json.Marshal(dev)
  fmt.Println(string(jsonDevice))
}

func main()   {
  // create a device with default settings
  rdevice := remote_device{"0.0.0.0","cisco","cisco","ssh"}
  // read ansible arguments supplied as a file
  data, err:= ioutil.ReadFile(os.Args[1])
  if err != nil { 
    panic(err) 
  }
  // split arguments into a slice
  args := strings.Split(string(data)," ")
  // iterate over arguments updating default device
  for _,arg := range args
      kvp := strings.Split(arg,"=")
      switch kvp[0] {
      case "ip":
        rdevice.IP = kvp[1]
      case "username":
        rdevice.Username = kvp[1]
      case "password":
        rdevice.Password = kvp[1]
      case "transport":
        rdevice.Transport = kvp[1]
      }
  }

  printDevice(rdevice)
  os.Exit(0)

}