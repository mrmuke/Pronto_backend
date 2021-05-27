import React,{useState} from 'react'
import airports from './airports';


export default function FlightSearch({onSelect}){
    const [filter,setFilter]= useState("")
    return(    <div className="dropdown open in mt-2">
      <input style={{ padding: '10px', background: 'transparent', border: 'none', outline: 'none',  color: 'white' }} type="text" 
           class="okay"  autocomplete="off" onChange={e=>setFilter(e.target.value)} value={filter} placeholder="Select airport: ..."/>
             
             <div >
          <div className="list-autocomplete">
          {filter.length>3&&airports.filter(a=>a.name.toLowerCase().includes(filter.toLowerCase())||a.city.toLowerCase().includes(filter.toLowerCase())).slice(0,3).map(airport=>(
          <button type="button" onClick={()=>{onSelect(airport.iata);setFilter(airport.iata)}} className="dropdown-item">{airport.name}<small style={{color:'#cdcdcd',marginLeft:'5px'}}>{airport.city}</small></button>))
          
          }
          </div>
        </div></div>)
}