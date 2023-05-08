import React from 'react'
import './maps.css'
import { MapContainer, TileLayer} from 'react-leaflet'
import MarkerList from './MarkerList'

const Maps = (props) => {
  /*
  const get_img_url = 'http://127.0.0.1:8001/api/get_media/'
  const handleClick = (file_name) => {
    const payload = {
      "pic": file_name
    }

    console.log(payload)
  
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }
  
    fetch(get_img_url, requestOptions).then(
        response=> {
          if(!response.ok) {
            alert('error occurred, pleases try again')
          }else{
            response.blob().then(
              media =>{
                return media
              }
            )
          }
        }
      )
    }
    */

  return (
    <div className='maps'>
      <MapContainer className='leaflet-container' center={[props.mapData[0].lat, props.mapData[0].lng]} zoom={6} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MarkerList mapData={props.mapData} />
 
      </MapContainer>
    </div>
  )
}

export default Maps