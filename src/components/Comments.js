import React, {useEffect, useState} from 'react'
import random from "random-name"
import './Comments.css'
export default function Comments({plan}){
    const [comment, setComment] = useState("");
    const [rating, setRating] = useState(10);
    const [mouse, setMouse] = useState(0);
    const [reviews, setReviews] = useState([]);

    useEffect(()=>{
        getComment();
    }, [])

    useEffect(()=>{
        console.log(reviews);
    }, [reviews])
    
    function submitComment(){
        let name = random.first() + " " + random.last();
        var request = new XMLHttpRequest();
        request.onreadystatechange = function(){
            if(request.readyState == 4 && request.status == 200){
                setReviews([{"name":name, "comment":comment, "rating": rating},...reviews]);
                setComment("");
            }
        }
        request.open("POST", "http://localhost:8000/api/plan/submitComment");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({
            name:name,
            comment: comment,
            rating: rating,
            id:plan.id,
        }))
    }

    function getComment(){
        var request = new XMLHttpRequest();
        request.onreadystatechange = function(){
            if(request.readyState == 4 && request.status == 200){
                setReviews(JSON.parse(request.response)["reviews"]);
            }
        }
        request.open("POST", "http://localhost:8000/api/plan/getComments");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({
            id:plan.id,
        }))
    }

    return (
        <div style={{height:'100%'}}><div style={{color:'white'}}>

        <details>
          <summary>Hotel</summary>
          <p>
          {plan.hotel}    </p>
        </details>
        <details>
          <summary>Transportation</summary>
          <p>
      {plan.transportation}    </p>
        </details>
        <details>
          <summary>Days
          </summary>
      <p>{plan.day_set&&plan.day_set.length} day trip </p> </details>
      
      
                  </div>
        <div className="container justify-content-center" style={{width:'100%',border:'3px solid #ccc'}}>
        <div className="d-flex justify-content-center pt-3 pb-2"> <input type="text" name="text" placeholder="+ Add a comment" className="form-control addtxt" value={comment} onChange={e => setComment(e.target.value)}/> </div>
        <div className="d-flex justify-content-center pt-3 pb-2">
            {
                (()=>{
                    let arr = [];
                    for(let i = 0; i < 10; i++){
                        let shade = rating;
                        if(mouse != 0){
                            shade = mouse;
                        }
                        if(i <= shade-1){
                            arr.push(<i style={{color:'gold', fontSize:"20px", margin:"0px 5px", cursor:'pointer'}} className="fa fa-star" onClick={
                                ()=>{
                                    setRating(i+1);
                                }
                            } onMouseOver={
                                ()=>{
                                    setMouse(i+1);
                                }
                            } onMouseOut={
                                ()=>{
                                    setMouse(0);
                                }
                            }></i>)
                        } else {
                            arr.push(<i style={{color:'white', fontSize:"20px", margin:"0px 5px", cursor:'pointer'}} className="fa fa-star" onClick={
                                ()=>{
                                    setRating(i+1);
                                }
                            } onMouseOver={
                                ()=>{
                                    setMouse(i+1);
                                }
                            } onMouseOut={
                                ()=>{
                                    setMouse(0);
                                }
                            }></i>)
                        }
                    }
                    console.log(arr)
                    return arr
                })()
            }
        </div>
        <div className="d-flex justify-content-center pt-3 pb-2"> <input type="button" name="button" className="form-control addtxt" value="Submit Comment" onClick={()=>{submitComment()}}/> </div>
        {
            (()=>{
                let item = [];
                if(reviews.length != 0){
                    for(let i = 0; i < reviews.length; i++){
                        item.push(
                            <div className="py-2">
                                <div className="second py-2 px-2"> <span className="text1">{reviews[i]["comment"]}</span>
                                    <div className="d-flex justify-content-between py-1 pt-2">
                                        <div><span className="text2">{reviews[i]["name"]}</span></div>
                                        <div><span className="text3">Rating</span><span className="thumbup"><i className="fa fa-thumbs-o-up"></i></span><span className="text4">{reviews[i]["rating"]}</span></div>
                                    </div>
                                </div>
                            </div>
                        )
                    }
                } else {
                    item.push(<p style={{color:'white'}}>No Comments Yet!</p>)
                }


                return item
            })()
        }
    </div></div>
    )
}