// pages/add/add.js
const app = getApp()

Page({
  data: {
    description: '',
    focus: true,
    selectedPriority: 'Medium',
    selectedCategory: 'General',
    priorities: [
      { label: '高', value: 'High', color: '#ff4d4f' },
      { label: '中', value: 'Medium', color: '#fa8c16' },
      { label: '低', value: 'Low', color: '#52c41a' }
    ],
    categories: [
      { label: '工作', value: 'Work' },
      { label: '学习', value: 'Study' },
      { label: '生活', value: 'Life' },
      { label: '通用', value: 'General' }
    ]
  },

  onInput(e) {
    this.setData({
      description: e.detail.value
    })
  },

  selectPriority(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      selectedPriority: value
    })
  },

  selectCategory(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      selectedCategory: value
    })
  },

  addTask() {
    const description = this.data.description.trim()

    if (!description) {
      wx.showToast({
        title: '请输入任务描述',
        icon: 'error'
      })
      return
    }

    const task = app.addTask(description)
    task.priority = this.data.selectedPriority
    task.category = this.data.selectedCategory

    app.saveTasks()

    wx.showToast({
      title: '添加成功',
      icon: 'success'
    })

    setTimeout(() => {
      wx.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  }
})
