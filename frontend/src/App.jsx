import React, { useEffect } from 'react'
import {Routes ,  Route} from 'react-router-dom'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/Register'
import { axiosClient } from './utils/axiosClient'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import MainContextProvider from './context/MainContext'


const App = () => {
  
  const checkServerHealth = async () => {
    const response = await axiosClient.get("/health")
    const data = await response.data
    console.log(data)
  }

  useEffect(() => {
    checkServerHealth()
  }
  , [])

  return (
    <MainContextProvider>
    <Navbar></Navbar>    

    <Routes>
      <Route path='/' Component={HomePage}></Route>
      <Route path='/login' Component={LoginPage}></Route>
      <Route path='/register' Component={RegisterPage}></Route>
    </Routes>


    <Footer/>
    </MainContextProvider>
  )
}

export default App
