import styles from './StatusPill.module.css';

const pillClass = {
  'Applied': styles.applied,
  'HR Screening': styles.hr,
  'Interview': styles.interview,
  'Offer': styles.offer,
  'On Hold': styles.onhold,
  'Rejected': styles.rejected,
};

export default function StatusPill({ status }) {
  return (
    <span className={`${styles.pill} ${pillClass[status] || styles.applied}`}>
      <span className={styles.dot} />
      {status}
    </span>
  );
}
