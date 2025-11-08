import { NextResponse } from 'next/server'

// This is a mock database. In a real application, you would use a proper database.
let grievances: any[] = []

// Simulated AI classification function
function classifyGrievance(description: string): { priority: string; category: string } {
  // In a real-world scenario, this would be an actual AI model
  const priorities = ['low', 'medium', 'high']
  const categories = ['technical', 'billing', 'service', 'other']
  
  return {
    priority: priorities[Math.floor(Math.random() * priorities.length)],
    category: categories[Math.floor(Math.random() * categories.length)]
  }
}

export async function GET() {
  return NextResponse.json(grievances)
}

export async function POST(request: Request) {
  const body = await request.json()
  const { title, description, category } = body

  const aiClassification = classifyGrievance(description)

  const newGrievance = {
    id: Date.now().toString(),
    title,
    description,
    category: category || aiClassification.category,
    status: 'open',
    priority: aiClassification.priority,
    createdAt: new Date().toISOString(),
  }

  grievances.push(newGrievance)

  return NextResponse.json(newGrievance, { status: 201 })
}