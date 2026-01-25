// pages/index/index.js
const app = getApp()

Page({
  data: {
    tasks: [],
    stats: {
      total: 0,
      completed: 0,
      pending: 0,
      completionRate: 0
    },
    showWarning: false,
    hasCompletedTasks: false
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

    this.setData({
      tasks,
      stats,
      showWarning: stats.pending > 5,
      hasCompletedTasks: tasks.some(t => t.status === 'done')
    })
  },

  toggleTask(e) {
    const id = e.currentTarget.dataset.id
    app.doneTask(id)
    this.loadData()
    wx.showToast({
      title: '任务状态已更新',
      icon: 'success'
    })
  },

  markDone(e) {
    const id = e.currentTarget.dataset.id
    if (app.doneTask(id)) {
      this.loadData()
      wx.showToast({
        title: '任务已完成',
        icon: 'success'
      })
    }
  },

  deleteTask(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个任务吗？',
      success: (res) => {
        if (res.confirm) {
          if (app.deleteTask(id)) {
            this.loadData()
            wx.showToast({
              title: '任务已删除',
              icon: 'success'
            })
          }
        }
      }
    })
  },

  clearCompleted() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有已完成的任务吗？',
      success: (res) => {
        if (res.confirm) {
          app.clearCompleted()
          this.loadData()
          wx.showToast({
            title: '已清除已完成任务',
            icon: 'success'
          })
        }
      }
    })
  }
})
