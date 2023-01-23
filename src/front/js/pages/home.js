import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

import { useNavigate } from "react-router-dom";

export const Home = () => {
	const { store, actions } = useContext(Context);

	const [username, setUsername] = useState("")
	const [password, setPassword] = useState("")
	const [errorLogin, setErrorLogin] = useState("")

	const navigate = useNavigate();

	const login=() =>{
		var myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");

		console.log(username, password)

		var raw = JSON.stringify({
		"username": username,
		"password": password
		});

		var requestOptions = {
		method: 'POST',
		headers: myHeaders,
		body: raw,
		redirect: 'follow'
		};

		fetch("https://3001-4geeksacade-reactflaskh-u5ios1wi99r.ws-eu77.gitpod.io/api/login", requestOptions)
		.then(response => response.json())
		//Aqui esta el token, en result
		.then(result => {
			if(result.token){
				localStorage.setItem("token",result.token);
				navigate("/demo");
			}else{
				setErrorLogin(result.msg)
			}
			
		})
		.catch(error => console.log('error', error));
			}

	return (
		<div className="text-center mt-5">
			<h1>Hello User!!</h1>
			<div>
				<label>Username: </label>
				<br></br>
				<input onChange = {(event) => setUsername(event.target.value)}></input>
			</div>
			<p></p>
			<div>
				<label>Password: </label>
				<br></br>
				<input onChange = {(event) => setPassword(event.target.value)}></input>
			</div>
			<p></p>
			<button onClick={login}>Login</button>
				{errorLogin && <div className="alert alert-danger" role="alert">
  					{errorLogin}
				</div>}
		</div>

	);
};
