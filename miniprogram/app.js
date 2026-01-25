// app.js
App({
  globalData: {
    tasks: []
  },

  onLaunch() {
    // 从本地存储加载数据
    this.loadTasks()
  },

  loadTasks() {
    try {
      const tasks = wx.getStorageSync('tasks')
      if (tasks) {
        this.globalData.tasks = tasks
      }
    } catch (e) {
      console.error('加载任务失败:', e)
    }
  },

  saveTasks() {
    try {
      wx.setStorageSync('tasks', this.globalData.tasks)
    } catch (e) {
      console.error('保存任务失败:', e)
      wx.showToast({
        title: '保存失败',
        icon: 'error'
      })
    }
  },

  addTask(description) {
    const tasks = this.globalData.tasks
    const newId = tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1
    const newTask = {
      id: newId,
      description: description,
      status: 'pending',
      createdAt: new Date().toISOString(),
      completedAt: null
    }
    tasks.push(newTask)
    this.saveTasks()
    return newTask
  },

  doneTask(id) {
    const task = this.globalData.tasks.find(t => t.id === id)
    if (task && task.status !== 'done') {
      task.status = 'done'
      task.completedAt = new Date().toISOString()
      this.saveTasks()
      return true
    }
    return false
  },

  deleteTask(id) {
    const index = this.globalData.tasks.findIndex(t => t.id === id)
    if (index !== -1) {
      this.globalData.tasks.splice(index, 1)
      this.saveTasks()
      return true
    }
    return false
  },

  clearCompleted() {
    const beforeCount = this.globalData.tasks.length
    this.globalData.tasks = this.globalData.tasks.filter(t => t.status !== 'done')
    this.saveTasks()
    return this.globalData.tasks.length < beforeCount
  },

  getStats() {
    const tasks = this.globalData.tasks
    const total = tasks.length
    const completed = tasks.filter(t => t.status === 'done').length
    const pending = tasks.filter(t => t.status === 'pending').length
    const completionRate = total > 0 ? ((completed / total) * 100).toFixed(2) : 0

    return {
      total,
      completed,
      pending,
      completionRate
    }
  }
})
