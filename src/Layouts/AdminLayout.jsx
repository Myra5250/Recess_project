import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Components/SideBar';

const AdminLayout = () => {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <main style={{ flex: 1, padding: '1rem' }}>
        <Outlet />
      </main>
    </div>
  );
};

export default AdminLayout;