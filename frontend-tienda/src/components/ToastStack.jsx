import PropTypes from 'prop-types';
import { Alert, Box } from '@mui/material';

export default function ToastStack({ notifications }) {
  return (
    <Box
      sx={{
        position: 'fixed',
        top: 20,
        right: 20,
        display: 'flex',
        flexDirection: 'column',
        gap: 1.25,
        zIndex: 1000,
        width: 340,
      }}
    >
      {notifications.map((n) => (
        <Alert key={n.id} severity={n.severity} elevation={3}>
          {n.text}
        </Alert>
      ))}
    </Box>
  );
}

ToastStack.propTypes = {
  notifications: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      severity: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
    }),
  ).isRequired,
};
