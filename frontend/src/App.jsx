import { useState, useEffect, useCallback } from 'react';
import './styles/globals.css';
import styles from './App.module.css';

import Sidebar              from './components/Sidebar';
import StatCards            from './components/StatCards';
import ApplicationList      from './components/ApplicationList';
import ApplicationForm      from './components/ApplicationForm';
import DetailDrawer         from './components/DetailDrawer';
import ArchivedApplications from './components/ArchivedApplications';
import Login                from './components/Login';

import { useAuth } from './AuthContext';

import {
  getApplications,
  deleteApplication,
  updateApplication,
} from './api/api';

export default function App() {
  const { user, logout } = useAuth();

  const [tab, setTab]                   = useState('active');
  const [apps, setApps]                 = useState([]);
  const [archiveCount, setArchiveCount] = useState(0);
  const [selectedApp, setSelectedApp]   = useState(null);
  const [refreshKey, setRefreshKey]     = useState(0);

  const refresh = useCallback(() => setRefreshKey(k => k + 1), []);

  // ── ALL hooks must be above any conditional returns ──────────────────────
  useEffect(() => {
    // Only fetch if user is signed in
    if (!user) return;

    getApplications()
      .then(res => setApps(res.data || []))
      .catch(console.error);
  }, [refreshKey, user]);

  // ── Conditional renders AFTER all hooks ──────────────────────────────────

  // Auth still loading
  if (user === undefined) {
    return (
      <div style={{ display:'flex', alignItems:'center', justifyContent:'center', minHeight:'100vh', background:'#0f172a', color:'#94a3b8', fontSize:'1rem' }}>
        Loading…
      </div>
    );
  }

  // Not signed in
  if (!user) {
    return <Login />;
  }

  // ── Signed in ─────────────────────────────────────────────────────────────

  const handleDelete = async (id) => {
    if (!window.confirm('Archive this application?')) return;
    try {
      await deleteApplication(id);
      if (selectedApp?.id === id) setSelectedApp(null);
      refresh();
    } catch (e) { console.error(e); }
  };

  const handleStatusChange = async (id, status) => {
    try {
      await updateApplication(id, { status });
      refresh();
    } catch (e) { console.error(e); }
  };

  return (
    <div className={styles.layout}>
      <Sidebar
        activeTab={tab}
        onTabChange={setTab}
        appCount={apps.length}
        archiveCount={archiveCount}
        user={user}
        onLogout={logout}
      />

      <main className={styles.main}>
        <div className={styles.topbar}>
          <h1 className={styles.pageTitle}>
            {tab === 'active' ? 'Active Applications' : 'Archived Applications'}
          </h1>
          {tab === 'active' && <ApplicationForm onCreated={refresh} />}
        </div>

        <div className={styles.content}>
          {tab === 'active' && (
            <>
              <StatCards apps={apps} />
              <ApplicationList
                applications={apps}
                onOpen={setSelectedApp}
                onDelete={handleDelete}
                refreshKey={refreshKey}
              />
            </>
          )}

          {tab === 'archive' && (
            <ArchivedApplications
              onRestore={refresh}
              onCountChange={setArchiveCount}
            />
          )}
        </div>
      </main>

      {selectedApp && (
        <DetailDrawer
          app={selectedApp}
          onClose={() => setSelectedApp(null)}
          onStatusChange={handleStatusChange}
          onRefresh={refresh}
        />
      )}
    </div>
  );
}
