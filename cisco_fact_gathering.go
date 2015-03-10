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
	USERNAME string
	PASSWORD string
	TRANSPORT string
}

func printDevice(dev remote_device ) {
  jsonDevice, _ := json.Marshal(dev)
  fmt.Println(string(jsonDevice))
}

func main()   {
  // create a default device
  rdevice := remote_device{"0.0.0.0","cisco","cisco","ssh"}
  // read ansible arguments
  data, err:= ioutil.ReadFile(os.Args[1])
  if err != nil { panic(err) }
  // split arguments in a slice
  args := strings.Split(string(data)," ")
  // iterate over arguments updating default device
  for _,arg := range args
      kvp := strings.Split(arg,"=")
      switch kvp[0] {
      case "ip":
        rdevice.IP = kvp[1]
      case "username":
        rdevice.USERNAME = kvp[1]
      case "password":
        rdevice.PASSWORD = kvp[1]
      case "transport":
        rdevice.TRANSPORT = kvp[1]
      }
  }

  printDevice(rdevice)
  os.Exit(0)

}