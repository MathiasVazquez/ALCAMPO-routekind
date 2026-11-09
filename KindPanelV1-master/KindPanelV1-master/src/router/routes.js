
const routes = [
  {
    path: '/',
    component: () => import('layouts/MapLayout.vue'),
    children: [
      { path: '', name: 'Index', component: () => import('pages/Index.vue') }
    ]
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'security', name: 'Security', component: () => import('pages/Security.vue') },
      { path: 'mobiles', name: 'Mobiles', component: () => import('pages/Mobiles.vue') },
      { path: 'planning', name: 'Planning', component: () => import('pages/Planning.vue') },
    ]
  },

  {
    path: '/login',
    component: () => import('layouts/LoginLayout.vue'),
    children: [{ path: '', name: 'Login', component: () => import('pages/Login') }]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
