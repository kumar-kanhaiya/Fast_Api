import React, { createContext, useContext, useEffect } from 'react'
import { useState } from 'react'
import { axiosClient } from '../utils/axiosClient'

const mainContext = createContext()

export const usemainContext = ()=> useContext(mainContext)

export const MainContextProvider = ({ children }) => {
  const [loading, setloading] = useState(true)

  const fetchProfile = async () => {
    const token = localStorage.getItem("token")

    if (!token) {
      setloading(false)
      return
    }

    try {
      const res = await axiosClient.get("/auth/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      console.log(res.data)
    } catch (error) {
      console.log(error)
    } finally {
      setloading(false)
    }
  }

  useEffect(() => {
    fetchProfile()
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <mainContext.Provider value={{ fetchProfile }}>
      {children}
    </mainContext.Provider>
  )
}
export default MainContextProvider
