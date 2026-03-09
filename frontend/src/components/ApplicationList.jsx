import { useState } from 'react';
import StatusPill from './StatusPill';
import styles from './ApplicationList.module.css';

const FILTERS = ['All', 'Applied', 'HR Screening', 'Interview', 'Offer', 'On Hold'];

function coColor(name) {
  const colors = ['#4f8ef7','#34d399','#fbbf24','#f87171','#a78bfa','#38bdf8','#fb923c'];
  let h = 0;
  for (let c of name) h = (h * 31 + c.charCodeAt(0)) & 0xff;
  return colors[h % colors.length];
}

export default function ApplicationList({ applications, onOpen, onDelete, refreshKey }) {
  const [filter, setFilter] = useState('All');
  const [search, setSearch] = useState('');

  const visible = applications.filter(a => {
    const q = search.toLowerCase();
    const matchSearch = !q || a.company.toLowerCase().includes(q) || a.role.toLowerCase().includes(q);
    const matchFilter = filter === 'All' || a.status === filter;
    return matchSearch && matchFilter;
  });

  return (
    <div className={styles.wrapper}>
      {/* Table panel */}
      <div className={styles.panel}>
        <div className={styles.panelHeader}>
          <span className={styles.panelTitle}>All Applications</span>
          <input
            className={styles.search}
            type="text"
            placeholder="🔍  Search…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <div className={styles.filterTabs}>
            {FILTERS.map(f => (
              <button
                key={f}
                className={`${styles.filterTab} ${filter === f ? styles.active : ''}`}
                onClick={() => setFilter(f)}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        <table className={styles.table}>
          <thead>
            <tr>
              <th>Company / Role</th>
              <th>Status</th>
              <th>Source</th>
              <th>Applied</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {visible.length === 0 ? (
              <tr>
                <td colSpan={5}>
                  <div className={styles.empty}>
                    <div className={styles.emptyIcon}>🔍</div>
                    No applications found
                  </div>
                </td>
              </tr>
            ) : visible.map(app => (
              <tr key={app.id} className={styles.row} onClick={() => onOpen(app)}>
                <td>
                  <div className={styles.companyCell}>
                    <div
                      className={styles.coLogo}
                      style={{ background: coColor(app.company) }}
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
                  <span className={styles.sourceTag}>{app.source || '—'}</span>
                </td>
                <td className={styles.dateCell}>{app.applied_date}</td>
                <td onClick={e => e.stopPropagation()}>
                  <div className={styles.actionBtns}>
                    <button className={styles.btnSm} onClick={() => onOpen(app)}>View</button>
                    <button className={`${styles.btnSm} ${styles.danger}`} onClick={() => onDelete(app.id)}>Delete</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
