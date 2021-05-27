import React, { useEffect, useState } from "react"
import "font-awesome/css/font-awesome.min.css"
import "./Search.css"
import cities from "./cities.json"

export default function Search(){
    const[search, setSearch] = useState("");
    const[cityArr, setCityArr] = useState([]);
    const[plan, setPlans] = useState([]);
    const[planNo, setPlanNo] = useState(3);

    useEffect(()=>{
        let request = new XMLHttpRequest();
        request.onreadystatechange = function(){
            if(request.readyState == 4 && request.status == 200){
                setPlans(JSON.parse(request.response)["Schedules"]);
                console.log(JSON.parse(request.response)["Schedules"])
                setSearch("")
            }
        }

        request.open("POST", "http://localhost:8000/api/plan/getPlans");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({
            "city":"all"
        }));
    },[])

    function getPlans(){
        let request = new XMLHttpRequest();
        request.onreadystatechange = function(){
            if(request.readyState == 4 && request.status == 200){
                setPlans(JSON.parse(request.response)["Schedules"]);
                console.log(JSON.parse(request.response)["Schedules"])
                setSearch("")
            }
        }

        request.open("POST", "http://localhost:8000/api/plan/getPlans");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({
            "city":search
        }));
    }

    return(
        <div style={{position:"relative", paddingTop:"50px", backgroundImage:'url("https://cdn.insuremytrip.com/resources/29223/italy_travel_insurance_venice.jpg")', backgroundSize:'cover', minHeight:'100vh'}}>
            <div className="search-container">
                <div className="searchbar-container">
                    <input className="searchbar" type="text" value={search} onChange={(e)=>{
                        let text = e.target.value
                        setSearch(text);
                        let count = 0;
                        let arr = [];
                        for(let city of cities){
                            if(city.name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().substring(0, text.length) == text.toLowerCase()){
                                count++;
                                arr.push(city);
                            }
                            if(count > 5){
                                break;
                            }
                        }
                        setCityArr(arr);
                    }} onKeyUp={(e)=>{
                        if(e.key == "Enter"){
                            getPlans()
                        }
                    }}></input>
                    <button className="search-button"><i className="fas fa-search" onClick={()=>{
                        getPlans()
                    }}></i></button>
                </div>
            </div>
            <div className="search-container">
                {
                    (()=>{
                        let arr = [];
                        if(cityArr != [] && search != ""){
                            for(let city of cityArr){
                                arr.push(<div className="autocomplete" onClick={()=>{
                                    setSearch(city.name.normalize("NFD").replace(/[\u0300-\u036f]/g, ""))
                                    setCityArr([])
                                }}>{city.name}, {city.country}</div>)
                            }
                        }
                        return arr
                    })()
                }
            </div>
            <div className="card-search-container">
                {
                    (()=>{
                        let arr = [];
                        for(let i = 0; i < planNo; i++){
                            let obj = plan[i];
                            if(obj == undefined){
                                break;
                            }
                            arr.push(<div className="card-search" onClick={
                                ()=>{
                                    window.location.href="http://localhost:3000/plan/"+obj.id
                                }
                            }>
                            <img class="card-search-image" src={obj.image}></img>
                            <div class="card-search-text">
                                <span>from {obj.origin}</span>
                                <h2>{obj.city.toUpperCase()}</h2>
                                <div><span>Departure: </span> {obj.departure.substring(5,10)}-{obj.departure.substring(0,4)}</div>
                                <div><span>Arrival: </span> {obj.arrvial.substring(5,10)}-{obj.departure.substring(0,4)}</div>
                                <div><span>Hotels: </span> {obj.hotel}</div>
                                <div><span>Transportation: </span> {obj.transportation}</div>
                            </div>
                            <div class="card-search-stats">
                                <div class="stat">
                                <div class="value">{obj.length}</div>
                                <div class="type">days</div>
                                </div>
                                <div class="stat">
                                <div class="value">{obj.comments}</div>
                                <div class="type">comments</div>
                                </div>
                                <div class="stat">
                                <div class="value">{
                                    (()=>{
                                        if(obj.rating == 0){
                                            return "N/A"
                                        } else {
                                            return Math.round(obj.rating * 10) / 10
                                        }
                                    })()
                                }</div>
                                <div class="type">rating</div>
                                </div>
                            </div>
                        </div>)
                        }
                        return arr;
                    })()
                }
            </div>
        </div>
    )
}