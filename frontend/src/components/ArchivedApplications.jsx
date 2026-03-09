import { useEffect, useState } from 'react';
import { getArchivedApplications, restoreApplication } from '../api/api';
import StatusPill from './StatusPill';
import styles from './ArchivedApplications.module.css';

function coColor(name) {
  const colors = ['#4f8ef7','#34d399','#fbbf24','#f87171','#a78bfa','#38bdf8','#fb923c'];
  let h = 0;
  for (let c of name) h = (h * 31 + c.charCodeAt(0)) & 0xff;
  return colors[h % colors.length];
}

export default function ArchivedApplications({ onRestore }) {
  const [apps, setApps]     = useState([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    getArchivedApplications()
      .then(res => { setApps(res.data); setLoading(false); })
      .catch(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleRestore = async (id) => {
    await restoreApplication(id);
    load();
    onRestore();
  };

  return (
    <div>
      <div className={styles.topbar}>
        <h1 className={styles.pageTitle}>Archived Applications</h1>
      </div>

      <div className={styles.panel}>
        <div className={styles.panelHeader}>
          <span className={styles.panelTitle}>Archive</span>
          <span className={styles.count}>{apps.length} entries</span>
        </div>

        {loading ? (
          <div className={styles.empty}><div className={styles.emptyIcon}>⏳</div>Loading…</div>
        ) : apps.length === 0 ? (
          <div className={styles.empty}><div className={styles.emptyIcon}>🗄</div>No archived applications</div>
        ) : (
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Company / Role</th>
                <th>Status at Archive</th>
                <th>Reason</th>
                <th>Archived On</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {apps.map(app => (
                <tr key={app.id} className={styles.row}>
                  <td>
                    <div className={styles.companyCell}>
                      <div
                        className={styles.coLogo}
                        style={{ background: coColor(app.company), opacity: 0.5 }}
                      >
                        {app.company[0]}
                      </div>
                      <div>
                        <div className={styles.coName}>{app.company}</div>
                        <div className={styles.coRole}>{app.role}</div>
                      </div>
                    </div>
                  </td>
                  <td><StatusPill status={app.status} /></td>
                  <td>
                    <span className={`${styles.reasonTag} ${app.archive_reason === 'Rejected' ? styles.rejected : styles.deleted}`}>
                      {app.archive_reason}
                    </span>
                  </td>
                  <td className={styles.dateCell}>
                    {app.archived_at ? new Date(app.archived_at).toLocaleDateString('en-IN', { dateStyle: 'medium' }) : '—'}
                  </td>
                  <td>
                    <button className={styles.restoreBtn} onClick={() => handleRestore(app.id)}>
                      ↩ Restore
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
