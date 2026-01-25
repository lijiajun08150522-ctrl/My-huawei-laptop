// pages/stats/stats.js
const app = getApp()

Page({
  data: {
    todayDate: '',
    stats: {
      total: 0,
      completed: 0,
      pending: 0,
      completionRate: 0
    },
    categoryStats: [],
    priorityStats: [],
    warning: false
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    this.loadData()
  },

  loadData() {
    const tasks = app.globalData.tasks || []
    const stats = app.getStats()

    // 今天的日期
    const today = new Date()
    const todayDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

    // 分类统计
    const categoryMap = {}
    tasks.forEach(task => {
      const category = task.category || 'General'
      categoryMap[category] = (categoryMap[category] || 0) + 1
    })

    const categoryStats = Object.keys(categoryMap).map((category, index) => {
      const count = categoryMap[category]
      const percentage = tasks.length > 0 ? (count / tasks.length * 100) : 0
      const colors = ['#1890ff', '#52c41a', '#fa8c16', '#eb2f96', '#722ed1']
      return {
        category,
        count,
        percentage: percentage.toFixed(1),
        color: colors[index % colors.length]
      }
    }).sort((a, b) => b.count - a.count)

    // 优先级统计
    const priorityMap = {}
    tasks.forEach(task => {
      const priority = task.priority || 'Medium'
      priorityMap[priority] = (priorityMap[priority] || 0) + 1
    })

    const priorityStats = Object.keys(priorityMap).map(priority => {
      const priorityLabels = {
        High: { label: '高', color: '#ff4d4f' },
        Medium: { label: '中', color: '#fa8c16' },
        Low: { label: '低', color: '#52c41a' }
      }
      return {
        priority: priorityLabels[priority]?.label || priority,
        count: priorityMap[priority],
        color: priorityLabels[priority]?.color || '#999'
      }
    })

    this.setData({
      todayDate,
      stats,
      categoryStats,
      priorityStats,
      warning: stats.pending > 5
    })
  }
})
