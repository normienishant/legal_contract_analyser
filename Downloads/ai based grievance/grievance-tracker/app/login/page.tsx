'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { User, MapPin, Lock, Eye, EyeOff } from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

const indianCities = [
  "Ahmedabad", "Bangalore", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Kolkata", 
  "Mumbai", "Pune", "Surat",
  // Add more Indian cities here
]

export default function LoginPage() {
  const [name, setName] = useState('')
  const [city, setCity] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [mobileNumber, setMobileNumber] = useState('')
  const [filteredCities, setFilteredCities] = useState(indianCities)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically handle the login/registration logic
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, city, password }),
      })
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('userName', name)
        localStorage.setItem('userId', data.userId)
        router.push('/')
      } else {
        throw new Error('Registration failed')
      }
    } catch (error) {
      console.error('Error during registration:', error)
      alert('Registration failed. Please try again.')
    }
  }

  const handleCityChange = (value: string) => {
    setCity(value)
    setFilteredCities(
      indianCities.filter(city => 
        city.toLowerCase().includes(value.toLowerCase())
      )
    )
  }

  const handleForgotPassword = async () => {
    // Implement forgot password logic here
    console.log('Forgot password for:', mobileNumber)
    // You would typically send a request to your backend here
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900">
      <Card className="w-full max-w-md mt-[-100px]">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Login / Register</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <Input
                  id="name"
                  type="text"
                  placeholder="Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="pl-10"
                  required
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="city">City</Label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <Select onValueChange={handleCityChange}>
                  <SelectTrigger className="pl-10">
                    <SelectValue placeholder="Select your city" />
                  </SelectTrigger>
                  <SelectContent>
                    {filteredCities.map((city) => (
                      <SelectItem key={city} value={city}>{city}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>
            <Button type="submit" className="w-full">Register</Button>
            <div className="text-center">
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="link" className="text-sm text-blue-600 hover:text-blue-800">
                    Forgot Password?
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Forgot Password</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="mobileNumber">Mobile Number</Label>
                      <Input
                        id="mobileNumber"
                        type="tel"
                        placeholder="Enter your mobile number"
                        value={mobileNumber}
                        onChange={(e) => setMobileNumber(e.target.value)}
                        required
                      />
                    </div>
                    <Button onClick={handleForgotPassword} className="w-full">
                      Reset Password
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
            <div className="text-center text-gray-500">OR</div>
            <Button type="button" variant="outline" className="w-full" onClick={() => {/* Implement Google login */}}>
              Continue with Google
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}