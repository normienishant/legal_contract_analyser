'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'

interface GrievanceFormProps {
  onSubmit: (formData: { title: string; description: string; category: string }) => void
}

export default function Component({ onSubmit }: GrievanceFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
  })

  const handleChange = (name: string, value: string) => {
    setFormData(prevData => ({ ...prevData, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      <div>
        <Label htmlFor="title" className="block text-sm font-medium mb-1">
          Title
        </Label>
        <Input
          id="title"
          name="title"
          value={formData.title}
          onChange={(e) => handleChange('title', e.target.value)}
          required
          className="w-full"
          placeholder="Enter the title of your grievance"
        />
      </div>
      <div>
        <Label htmlFor="description" className="block text-sm font-medium mb-1">
          Description
        </Label>
        <Textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={(e) => handleChange('description', e.target.value)}
          required
          rows={4}
          className="w-full"
          placeholder="Provide details about your grievance"
        />
      </div>
      <div>
        <Label htmlFor="category" className="block text-sm font-medium mb-1">
          Category
        </Label>
        <Select onValueChange={(value) => handleChange('category', value)}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select a category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="technical">Technical Issue</SelectItem>
            <SelectItem value="billing">Billing Problem</SelectItem>
            <SelectItem value="service">Customer Service</SelectItem>
            <SelectItem value="other">Other</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Button
          type="submit"
          className="w-full flex items-center justify-center"
        >
          <PaperAirplaneIcon className="h-5 w-5 mr-2" />
          Submit Grievance
        </Button>
      </motion.div>
    </motion.form>
  )
}