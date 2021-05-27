import axios from "axios";
import React,{ useEffect, useState } from "react"
import { Redirect, useParams } from "react-router-dom";
import { Button } from "./Button";
import MapChart from "./MapChart";
import './City.css'
import FlightSearch from "./FlightSearch";
export default function City(){
    const [city,setCity] = useState(null)
    const [plan,setPlan] = useState(null)
    const [loading,setLoading] = useState(false)
    const [numDays,setNumDays]=useState(3)
    const [fromCity,setFromCity] = useState("")
    let { name } = useParams();
    useEffect(()=>{
        getCity()
    },[])
    function getCity(){
        axios.get("http://localhost:8000/api/cities/city?city=" + name)
        .then(result => {
          setCity(result.data)
          console.log(result.data)
        })
    }
    function createPlan(){
        setLoading(true)
        axios.get(`http://localhost:8000/api/plan/getSchedule?city=${name}&days=${numDays}&from=${fromCity}`)
        .then(result=>{ 
            setPlan(result.data);
        })
    }
    if(!city){
        return null
    }
    if(plan){
        return <Redirect to={`/plan/${plan}`}/>
    }
    return (
        <div style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center', background:` linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5) ), url(${city.images[1]})`, minHeight:'100vh',backgroundSize:'cover'}}>
            <div className="info-container">
              <div className="card mb-3">
                <div>
                  <img src={city.images[0]} className="card-img" alt="..." />
                </div>
                <div className="row no-gutters">
    
                  <div className="card-body">
                    <h5 className="card-title">{name.replace("-"," ")}</h5>
                    <p className="card-text">{city.summary}</p>
                    <p className="card-text"><small className="text-muted">Last updated 3 mins ago</small></p>
                  </div>
                </div>
              </div> 
              <div style={{width:'100%',display:'flex',flexDirection:'column', alignItems:'center'}}>

              <MapChart point={city.coords} city={name.replace("-"," ")}/>
              <div style={{display:'flex',alignItems:'center',flexDirection:'column',marginBottom:'10px'}}>
                <div>
              <strong style={{color:'white', marginRight:'3px'}}>Num Days: </strong><input style={{ padding: '10px', background: 'transparent', border: 'none', outline: 'none',  color: 'white' }} value={numDays} min="1" max="5" onChange={e => setNumDays(e.target.value)} type="number" placeholder={"#"} /></div><div  style={{borderTop:'1px solid #eee'}}>
                <FlightSearch onSelect={from=>setFromCity(from)}/>
                {/* {fromCity&&<p style={{textAlign:'center',color:'white'}}>You have selected {fromCity}</p>} */}
              {/* <strong style={{color:'white', marginRight:'3px'}}>Origin Airport: </strong><input style={{ padding: '10px', background: 'transparent', border: 'none', outline: 'none', borderBottom: '2px solid white', color: 'white' }} value={fromCity}  onChange={e => setFromCity(e.target.value)} placeholder={"City"} />*/}</div>

              </div>

              <Button
                  className='btns'
                  buttonStyle='btn--primary'
                  buttonSize='btn--large'
                  onClick={createPlan}
                >

{!loading?"CREATE PLAN":<div>PLANNING <div class="spinner-border" role="status">
              <span class="sr-only">Loading...</span>
            </div></div>}        </Button></div></div>
              
              </div>
    )
}
