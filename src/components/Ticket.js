import './Ticket.css'
import React from 'react'
export default function Ticket({flight}){
  if(!flight){
    return null
  }
  var months = [ "January", "February", "March", "April", "May", "June", 
           "July", "August", "September", "October", "November", "December" ]
    return <div style={{display:'flex',alignItems:'center',flexDirection:'column'}}>
      
        <h1 className="ticket-header">Departure</h1>
        <article className="ticket card">
          <section className="date">
            <time>
              <span>{flight.OutDay.substr(flight.OutDay.indexOf("/")+1)}</span><span>{months[parseInt(flight.OutDay.substr(0,flight.OutDay.indexOf("/")))-1]}</span>
            </time>
          </section>
          <section className="card-cont">
            <small>Departure</small>
            <h3>Flight - {flight.OutCities}</h3>
            <div className="even-date">
             <i className="fa fa-calendar"></i>
             <span>{flight.OutWeekday} {flight.OutTime.replace("+1", "the next day")}</span>
            </div>
            <div className="even-date">
             <i className="fa fa-clock"></i>
               <span>{flight.OutDuration}</span>
            </div>
            <div className="even-date">
             <i className="fa fa-map-marker"></i>
               <span>{flight.OutStops} to {flight.OutStopCities}</span>
            </div>
            <div className="even-info">
              <i className="fa fa-fighter-jet"></i>
              <p>
              {flight.OutAirline}
              </p>
            </div>
            <a href="#">Purchase</a>
          </section>
        </article>
        <h1 className="ticket-header">Arrival</h1>
        <article className="ticket card card">
        <section className="date">
            <time>
              <span>{flight.ReturnDay.substr(flight.ReturnDay.indexOf("/")+1)}</span><span>{months[parseInt(flight.ReturnDay.substr(0,flight.ReturnDay.indexOf("/")))-1]}</span>
            </time>
          </section>
          <section className="card-cont">
            <small>Departure</small>
            <h3>Flight - {flight.ReturnCities}</h3>
            <div className="even-date">
             <i className="fa fa-calendar"></i>
             <span>{flight.ReturnWeekday} {flight.ReturnTime.replace("+1", "the next day")}</span>
            </div>
            <div className="even-date">
             <i className="fa fa-clock"></i>
               <span>{flight.ReturnDuration}</span>
            </div>
            <div className="even-date">
             <i className="fa fa-map-marker"></i>
               <span>{flight.ReturnStops} to {flight.ReturnStopCities}</span>
            </div>
            <div className="even-info">
              <i className="fa fa-fighter-jet"></i>
              <p>
              {flight.ReturnAirline}
              </p>
            </div>
            <a href="#">Purchase</a>
          </section>
        </article>
      </div>
      
}