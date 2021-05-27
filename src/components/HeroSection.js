import axios from 'axios';
import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
  const [adjectives, setAdjectives] = useState([""])
  const [loading, setLoading] = useState(false)
  const [city, setCity] = useState("")
  const [redirect, setRedirect] = useState(false)
  function changeAdjective(value, index) {
    let arr = [...adjectives]; // copying the old datas array
    arr[index] = value
    setAdjectives(arr)
  }
  function removeAdjective(index) {
    let arr = [...adjectives];
    arr.splice(index, 1)
    setAdjectives(arr)
  }
  function getDestinations() {
    console.log("Getting Data")
    setLoading(true)
    axios.get("http://localhost:8000/api/cities/dictionaryDestination?adjs=" + JSON.stringify(adjectives))
      .then(result => {
        setCity(result.data)
        setLoading(false)
        setRedirect(true)
      }).catch(e=>{
        alert("We don't recognize some of your adjectives..")
        setLoading(false)
      })
  }
  if(redirect){
    return <Redirect to={"/city/"+city.replace(" ","-")}/>
  }
  return (
    <div className="hero-main-container">
      <img className="background" src='/images/beach.jpg' />

      <div className='hero-container'>


        <h1>ADVENTURE AWAITS</h1>
        <p>What are you waiting for?</p>
        {
          !loading ?
            <div className='hero-btns'>
              {adjectives.map((adj, index) => (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', borderRadius: '10px', marginBottom: '5px' }}>
                  <input style={{ padding: '10px', background: 'transparent', border: 'none', outline: 'none', borderBottom: '2px solid white', color: 'white' }} value={adj} onChange={e => changeAdjective(e.target.value, index)} placeholder={`Adj ` + (index + 1)} />
                  <i className="fa fa-times-circle" onClick={() => { if (adjectives.length > 1) { removeAdjective(index) } }} style={{ fontSize: 35, margin: '5px', color: 'white' }} />
                </div>

              ))}
              <div style={{ display: 'flex' }}>
                <Button
                  className='btns'
                  buttonStyle='btn--primary'
                  buttonSize='btn--large'
                  onClick={() => { if (adjectives[adjectives.length - 1].length > 0) { setAdjectives(prevArray => [...prevArray, ""]) } }}
                >
                  <i className='fa fa-plus' /> ADD ADJ
        </Button>
                <Button
                  className='btns'
                  buttonStyle='btn--outline'
                  buttonSize='btn--large'
                  onClick={()=>{if(adjectives.find(i=>i.length==0)==null){getDestinations()}}}
                >
                  DISCOVER
        </Button></div>
            </div> : <div class="spinner-border" role="status">
              <span class="sr-only">Loading...</span>
            </div>}
      </div></div>
  );
}

export default HeroSection;
