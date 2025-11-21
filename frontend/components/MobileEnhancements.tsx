'use client'

import { useEffect, useState } from 'react'

// Hook for swipe gestures
export function useSwipe(onSwipeLeft?: () => void, onSwipeRight?: () => void) {
  const [touchStart, setTouchStart] = useState<number | null>(null)
  const [touchEnd, setTouchEnd] = useState<number | null>(null)

  const minSwipeDistance = 50

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null)
    setTouchStart(e.targetTouches[0].clientX)
  }

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX)
  }

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return
    const distance = touchStart - touchEnd
    const isLeftSwipe = distance > minSwipeDistance
    const isRightSwipe = distance < -minSwipeDistance

    if (isLeftSwipe && onSwipeLeft) {
      onSwipeLeft()
    }
    if (isRightSwipe && onSwipeRight) {
      onSwipeRight()
    }
  }

  return {
    onTouchStart,
    onTouchMove,
    onTouchEnd,
  }
}

// Mobile bottom sheet component
interface BottomSheetProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  title?: string
}

export function BottomSheet({ isOpen, onClose, children, title }: BottomSheetProps) {
  if (!isOpen) return null

  return (
    <>
      <div
        className="fixed inset-0 bg-black/50 z-40 md:hidden"
        onClick={onClose}
      />
      <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-[#141414] rounded-t-3xl shadow-2xl z-50 md:hidden max-h-[80vh] overflow-y-auto">
        <div className="sticky top-0 bg-white dark:bg-[#141414] border-b border-gray-200 dark:border-[#262626] p-4 flex items-center justify-between">
          {title && (
            <h3 className="text-lg font-bold text-gray-900 dark:text-[#e5e5e5]">{title}</h3>
          )}
          <button
            onClick={onClose}
            className="ml-auto p-2 text-gray-500 dark:text-[#a3a3a3] hover:text-gray-700 dark:hover:text-[#e5e5e5]"
          >
            ✕
          </button>
        </div>
        <div className="p-4">{children}</div>
      </div>
    </>
  )
}

// Pull to refresh hook
export function usePullToRefresh(onRefresh: () => Promise<void>) {
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [startY, setStartY] = useState(0)
  const [pullDistance, setPullDistance] = useState(0)

  useEffect(() => {
    let touchStartY = 0
    let isPulling = false

    const handleTouchStart = (e: TouchEvent) => {
      if (window.scrollY === 0) {
        touchStartY = e.touches[0].clientY
        isPulling = true
      }
    }

    const handleTouchMove = (e: TouchEvent) => {
      if (!isPulling) return
      const currentY = e.touches[0].clientY
      const distance = currentY - touchStartY

      if (distance > 0 && window.scrollY === 0) {
        setPullDistance(Math.min(distance, 100))
        e.preventDefault()
      }
    }

    const handleTouchEnd = async () => {
      if (pullDistance > 50 && !isRefreshing) {
        setIsRefreshing(true)
        await onRefresh()
        setIsRefreshing(false)
      }
      setPullDistance(0)
      isPulling = false
    }

    window.addEventListener('touchstart', handleTouchStart, { passive: false })
    window.addEventListener('touchmove', handleTouchMove, { passive: false })
    window.addEventListener('touchend', handleTouchEnd)

    return () => {
      window.removeEventListener('touchstart', handleTouchStart)
      window.removeEventListener('touchmove', handleTouchMove)
      window.removeEventListener('touchend', handleTouchEnd)
    }
  }, [pullDistance, isRefreshing, onRefresh])

  return { isRefreshing, pullDistance }
}

