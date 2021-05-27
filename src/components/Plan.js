import axios from "axios";
import React,{ createRef, useEffect, useReducer, useRef, useState } from "react"
import { useParams } from "react-router-dom";
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';

import './plan.css'
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from 'react-responsive-carousel';
import AppMap from "./AppMap";
import Ticket from "./Ticket";
import Comments from "./Comments";
import { Button } from "./Button";
export default function Plan(){
    
    const [plan,setPlan] = useState(null)
    const [showSchedule,setShowSchedule] = useState(false)
    const [flight,setFlight]=useState(null)
    let { id } = useParams();
    
    

    useEffect(()=>{
        getPlan()

    },[])
    
    function getPlan(){
        axios.get("http://localhost:8000/api/plan/"+id)
        .then(result => {
          setPlan(result.data.plan)
          console.log(result.data.plan)
          setFlight(result.data.flight)
        })
    }
    if(!plan){
        return <div style={{display:'flex',alignItems:'center',justifyContent:'center',flexDirection:'column',height:'100vh'}}><h2>OPTIMIZING FLIGHT</h2><div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div></div>
    }

    return (
        <div style={{background:` linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5) ), url(https://static01.nyt.com/images/2020/02/07/world/07hongkong-1/merlin_168336351_fce8cc0c-5e7f-404e-b299-6ea3b7245bea-superJumbo.jpg)`, minHeight:'100vh',backgroundSize:'cover',padding:'15px'}}>
          
                <div style={{display:'flex',justifyContent:'center'}}><h1 style={{marginBottom:'5px',color:'white'}}>My Trip to {plan.city}</h1></div>
            

<Carousel autoPlay={false}>

{plan.day_set.map((day,index)=>(

<div className="schedule-map-container" key={day.id}>
    
<Day plan={plan} setPlan={setPlan} index={index} showSchedule={showSchedule} day={day}/>
        
        <button onClick={()=>setShowSchedule(!showSchedule)} className="show-schedule btn btn-light"><i className="fa fa-arrow-up mr-2"></i>Show/Hide Schedule</button>
        </div>))}
</Carousel>
<div style={{display:'flex',justifyContent:'center',marginBottom:'15px'}}>
<Button
                  className='btns'
                  
                  buttonStyle='btn--primary'
                  buttonSize='btn--large'
                >Book Flight and Hotel! ${flight&&flight.Price} + $100 </Button></div>
<div className="row">
{/*certain height but overflow or no comments yet */}
<div className="col-lg-8">
<Ticket flight={flight}/></div>
<div className="col-lg-4">
<Comments plan={plan}/></div>{/*  get flight when page loads and balance length with price, schedule info- length of trip, etc */}
</div>
              </div>
    )
}
function Day({plan,setPlan,index,showSchedule,day}){
  const todoRef = createRef(null);
  const [editLocation, setEditLocation] = useState(null);
  const [editLoc,setEditLoc]= useState(null)
  const [height,setHeight]=useState(null)
    // useEffect will run on stageCanvasRef value assignment
    useEffect( () => {

        // The 'current' property contains info of the reference:
        // align, title, ... , width, height, etc.
        if(todoRef.current){

            setHeight(todoRef.current.offsetHeight)
            console.log(todoRef.current.offsetHeight)
        }

    }, [todoRef]);

    function updatePlanLocation(val,id,index){
      let label = val.label.substr(0,val.label.indexOf(","))
      let loc=null
        setEditLocation(label)
        const newList = plan.day_set[index].location_set.map((item) => {
          console.log(item.id)
          console.log(id)
          if (item.id === id) {
            const updatedItem = {
              ...item,
              name:label,
              type:val.value.types[0]
            };
            loc=updatedItem
     
            return updatedItem;
          }
     
          return item;
        });
        console.log(newList)
        const newPlan = Object.assign({}, plan);
        newPlan["day_set"][index]["location_set"] = newList;
        setPlan(newPlan)
        axios.put('http://localhost:8000/api/plan/'+loc.id,loc)
        setEditLoc(null)
    }
  return (<><div ref={todoRef}  className="todo-cmp" style={{visibility:(showSchedule?"visible":""),position:(showSchedule?"initial":""),width:(showSchedule?"100%":"")}}>

  <header  className="todo-cmp__header">
    <h2>Day {index+1}</h2>
    <p>Have fun!</p>
  </header>

    <ul  className="todo-cmp__list">
                {day.location_set.map(loc=>(
                    loc.id==editLoc?
<GooglePlacesAutocomplete
    selectProps={{
      editLocation,
      onChange: (val)=>updatePlanLocation(val,loc.id,index),
    }}
  />
                    :
                    <li key={loc.id}>

        <label style={{marginRight:'10px'}}>
          <input type="checkbox"/>
          <span style={{display:'flex',justifyContent:'space-between',alignItems:'baseline'}}>{loc.name}        <button style={{background:'none',border:'0',marginRight:'20px'}} onClick={()=>setEditLoc(loc.id)}><i className="fa fa-edit"></i></button>
</span>
                        <span style={{opacity:'0.6'}}>{loc.type}</span>

        </label>

      </li>
                ))}
      
  </ul>
</div>{!showSchedule&&<AppMap height={height} places={day.location_set}/>}</>)
}



