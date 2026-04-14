import { useState, useCallback } from 'react'
import storyData from '../story-data.json'

export function useStory() {
  const [currentPage, setCurrentPage] = useState(storyData.startPage)
  const [history, setHistory] = useState([storyData.startPage])

  const page = storyData.pages[String(currentPage)]

  const goToPage = useCallback((pageNum) => {
    setCurrentPage(pageNum)
    setHistory(h => [...h, pageNum])
  }, [])

  const goBack = useCallback(() => {
    setHistory(h => {
      if (h.length <= 1) return h
      const newHistory = h.slice(0, -1)
      setCurrentPage(newHistory[newHistory.length - 1])
      return newHistory
    })
  }, [])

  const restart = useCallback(() => {
    setCurrentPage(storyData.startPage)
    setHistory([storyData.startPage])
  }, [])

  return { page, currentPage, history, goToPage, goBack, restart, allPages: storyData.pages }
}