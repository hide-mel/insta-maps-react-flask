import './App.css'
import Navbar from './components/nav/Navbar'
import React, {useState} from "react"
import Maps from './components/maps/Maps'
import Loading from './components/loading/Loading'

function App() {
  const get_url = 'http://127.0.0.1:8001/api/get_data/'
  const get_all_url = 'http://127.0.0.1:8001/api/get_geo/'

  const [maps, setMaps] = useState(false)
  const [mapData, setMapdata] = useState({})

  const getData = (username,pass,target) => {

    let url = get_url
    if (username != "" && pass != "" ){
      url = get_all_url
    }

    const payload = {
        "username": username,
        "passwd": pass,
        "target": target
    }
    //console.log(payload)

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }

    fetch(url, requestOptions).then(
      response=> {
        if(!response.ok) {
          alert('error occurred, pleases try again')
        }else{
          response.json().then(
            data => {
              if (Object.keys(data).length!==0) {
                console.log(data)
                setMapdata(data)
                setMaps(true)
              }else{
                alert('error occurred, pleases try again')
              }
            }
          )
        }
      }
    )
    


  }

  return (
    <>
      <Navbar getData={getData}/>
      {
        maps && mapData!=="{}" ? <Maps mapData={mapData}/> : <Loading />
      }
    </>
  );
}

export default App;
