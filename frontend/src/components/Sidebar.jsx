import applytLogo from '../assets/applyt-logo.png';
import styles from './Sidebar.module.css';

export default function Sidebar({ activeTab, onTabChange, appCount, archiveCount, user, onLogout }) {
  const displayName = user?.displayName || user?.phoneNumber || user?.email || "Account";
  const photoURL    = user?.photoURL;

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>
        <img src={applytLogo} alt="APPLYT" className={styles.logoImg} />
        <div className={styles.logoTextWrap}>
          <span className={styles.logoName}>APPLYT</span>
          <span className={styles.logoSub}>Job Hunt Dashboard</span>
        </div>
      </div>

      <div className={styles.navSection}>Tracking</div>

      <div
        className={`${styles.navItem} ${activeTab === 'active' ? styles.active : ''}`}
        onClick={() => onTabChange('active')}
      >
        <span className={styles.navIcon}>📂</span>
        Applications
        <span className={styles.navCount}>{appCount}</span>
      </div>

      <div
        className={`${styles.navItem} ${activeTab === 'archive' ? styles.active : ''}`}
        onClick={() => onTabChange('archive')}
      >
        <span className={styles.navIcon}>🗄</span>
        Archived
        <span className={styles.navCount}>{archiveCount}</span>
      </div>

      <div className={styles.sidebarFooter}>
        {user && (
          <div className={styles.userRow}>
            {photoURL ? (
              <img src={photoURL} alt="" className={styles.avatar} />
            ) : (
              <div className={styles.avatarPlaceholder}>
                {displayName[0]?.toUpperCase()}
              </div>
            )}
            <div className={styles.userInfo}>
              <span className={styles.userName}>{displayName}</span>
              <button
                className={styles.logoutBtn}
                onClick={() => { if (window.confirm('Are you sure you want to sign out?')) onLogout(); }}
              >
                Sign out
              </button>
            </div>
          </div>
        )}
        <div className={styles.footerBadge}>
          <span className={styles.footerDot} />
          Backend connected
        </div>
      </div>
    </aside>
  );
}
