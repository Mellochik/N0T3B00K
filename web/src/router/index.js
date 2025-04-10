import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import MainView from '@/views/MainView.vue'
import HomeView from '@/views/home/HomeView.vue'
import TasksWorkspacesView from '@/views/tasks/SpacesView.vue'
import TasksStacksView from '@/views/tasks/StacksView.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView
    },
    {
        path: '/',
        component: MainView,
        children: [
            {
                path: '',
                name: 'Home',
                component: HomeView
            },
            {
                path: 'tasks',
                name: 'Tasks',
                children: [
                    {
                        path: 'workspaces',
                        name: 'TasksWorkspaces',
                        component: TasksWorkspacesView,
                        children: [
                            {
                                path: ':id',
                                name: 'TasksStacks',
                                component: TasksStacksView,
                                props: true
                            }
                        ]
                    }
                ]
            },
            {
                path: '/docs',
                name: 'Docs'
            }
        ],
    },
    {
        path: '/profile',
        name: 'Profile',
        component: HomeView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


// router.beforeEach(async (to, from, next) => {
//     const token = localStorage.getItem('access_token');

//     if (!token && to.name !== 'Login' && to.name !== 'Register') {
//         next({ name: 'Login' });
//     } else {
//         next();
//     }
// });

export default router
