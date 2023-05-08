import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import { Marker,Popup } from 'react-leaflet'

const MarkerList = (props) => {
  const mediaUrl_pre = "http://127.0.0.1:8001/api/get_media/?pic="

  return (
    
    props.mapData.map(x => (
        <Marker position={[x.lat,x.lng]} key={uuidv4()} data={x} eventHandlers={{
                //click: (e) => {
                //    e.target.options.data.media = props.handleClick(e.target.options.data.file_name)
                //},
            }}>
            <Popup className='popup-window' maxWidth="600" maxHeight="auto" closeButton='false'>
                <div className='popup-div'>
                    <img className='popup-media' src={mediaUrl_pre + x.file_name} alt={x.file_name} />
                </div>
            </Popup>
        </Marker>
      ))
  )
}

export default MarkerList