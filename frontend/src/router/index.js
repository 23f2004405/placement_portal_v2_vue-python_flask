import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/auth/Login.vue')
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/Login.vue')
    },
    {
      path: '/register_company',
      name: 'register_company',
      component: () => import('../views/auth/RegisterCompany.vue')
    },
    {
      path: '/register_student',
      name: 'register_student',
      component: () => import('../views/auth/RegisterStudent.vue')
    },
    //company

    {
      path: '/company/drives',
      name: 'company_drives',
      component: () => import('../views/company/CompanyDrives.vue')
    },
    {
      path: '/company/drives/:drive_id',
      name: 'company_drive_details',
      component: () => import('../views/company/DriveDetails.vue')
    },
    {
      path: '/company/drives/:drive_id/applications',
      name: 'company_drive_applications',
      component: () => import('../views/company/ViewApplications.vue')
    },
    {
      path: '/company/application/:application_id',
      name: 'company_drive_application_detail',
      component: () => import('../views/company/ApplicationDetails.vue')
    },
    {
      path: '/company/create_drive',
      name: 'create_drive',
      component: () => import('../views/company/CreateDrive.vue')
    },
    {
      path: '/company/:company_id',
      name: 'company_dashboard',
      component: () => import('../views/company/CompanyDashboard.vue')
    },
    // student

    {
      path: '/student/apply_drives',
      name: 'student_apply_drives',
      component: () => import('../views/student/StudentDrives.vue')
    },
    {
      path: '/student/drive/:drive_id',
      name: 'student_drive',
      component: () => import('../views/student/DriveDetails.vue')
    },
    {
      path: '/student/history/applications',
      name: 'student_history',
      component: () => import('../views/student/ApplicationHistory.vue')
    },
    {
      path: '/student/edit_profile',
      name: 'student_edit_profile',
      component: () => import('../views/student/EditProfile.vue')
    },
    {
      path: '/student/upload_resume',
      name: 'student_upload_resume',
      component: () => import('../views/student/UploadResume.vue')
    },
    {
      path: '/student/:student_id',
      name: 'student_dashboard',
      component: () => import('../views/student/StudentDashboard.vue')
    },
    // admin
    {
      path: '/admin/dashboard',
      name: 'admin_dashboard',
      component: () => import('../views/admin/AdminDashboard.vue')
    },
    {
      path: '/admin/companies',
      name: 'admin_companies',
      component: () => import('../views/admin/Companies.vue')
    },
    {
      path: '/admin/company/:company_id',
      name: 'admin_company',
      component: () => import('../views/admin/CompanyDetails.vue')
    },
    {
      path: '/admin/students',
      name: 'admin_students',
      component: () => import('../views/admin/Students.vue')
    },
    {
      path: '/admin/student/:student_id',
      name: 'admin_student',
      component: () => import('../views/admin/StudentDetails.vue')
    },
    {
      path: '/admin/company/registrations',
      name: 'admin_company_registrations',
      component: () => import('../views/admin/CompanyRegistrations.vue')
    },
    {
      path: '/admin/drives',
      name: 'admin_drives',
      component: () => import('../views/admin/PlacementDrives.vue')
    },
    {
      path: '/admin/drive/:drive_id',
      name: 'admin_drive',
      component: () => import('../views/admin/DriveDetails.vue')
    },
    {
      path: '/admin/drive/:drive_id/applications',
      name: 'admin_drive_applications',
      component: () => import('../views/admin/Applications.vue')
    },

  ],
})

export default router
