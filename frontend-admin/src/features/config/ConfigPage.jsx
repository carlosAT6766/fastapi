import { useEffect, useState } from 'react';
import { Typography, Paper, Button } from '@mui/material';
import { SelectField } from '../../components/SelectField';
import { SOURCE_OPTIONS, STYLE_OPTIONS } from '../../constants';
import { sx } from '../../theme';

export function ConfigPage({ settings, onSave }) {
  const [source, setSource] = useState(settings.defaultSource);
  const [style, setStyle] = useState(settings.defaultStyle);

  useEffect(() => {
    setSource(settings.defaultSource);
    setStyle(settings.defaultStyle);
  }, [settings]);

  return (
    <div>
      <Typography variant="h5" sx={sx.heading}>
        Configuración
      </Typography>
      <Typography variant="body2" sx={sx.subtitle}>
        Fuente y estilo por defecto usados al crear un nuevo resumen.
      </Typography>

      <Paper elevation={0} sx={sx.card}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 360 }}>
          <SelectField
            label="Fuente por defecto"
            fullWidth
            size="small"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            options={SOURCE_OPTIONS}
          />
          <SelectField
            label="Estilo por defecto"
            fullWidth
            size="small"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            options={STYLE_OPTIONS}
          />
          <div>
            <Button
              variant="contained"
              disableElevation
              onClick={() => onSave({ defaultSource: source, defaultStyle: style })}
              sx={sx.primaryBtn}
            >
              Guardar configuración
            </Button>
          </div>
        </div>
      </Paper>
    </div>
  );
}
