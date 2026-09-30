import { useCallback, useEffect, useState } from 'react';
import { Users, Package, Boxes, TriangleAlert } from 'lucide-react';
import { api } from '../services/api';
import StatCard from '../components/StatCard';
import AlertPanel from '../components/AlertPanel';
import CargoTable from '../components/CargoTable';
import InventoryPanel from '../components/InventoryPanel';
import LiveMap from '../components/LiveMap';

const emptyDashboard = {
  stats: {},
  cargo: [],
  inventory: [],
  alerts: [],
  live: { cargo: [], personnel: [] },
};

export default function Dashboard({ setPage }) {
  const [data, setData] = useState(emptyDashboard);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  const load = useCallback(async () => {
    try {
      const [stats, cargo, inventory, alerts, live] = await Promise.all([
        api.stats(),
        api.cargo(),
        api.inventory(),
        api.alerts(),
        api.live(),
      ]);

      setData({
        stats: stats || {},
        cargo: Array.isArray(cargo) ? cargo : [],
        inventory: Array.isArray(inventory) ? inventory : [],
        alerts: Array.isArray(alerts) ? alerts : [],
        live: {
          cargo: Array.isArray(live?.cargo) ? live.cargo : [],
          personnel: Array.isArray(live?.personnel) ? live.personnel : [],
        },
      });
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Dashboard API error:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
    const timer = window.setInterval(load, 10000);
    return () => window.clearInterval(timer);
  }, [load]);

  const resolve = async (id) => {
    try {
      await api.resolveAlert(id);
      await load();
    } catch (error) {
      console.error('Could not resolve alert:', error);
    }
  };

  const updateCargo = async (id, status) => {
    try {
      await api.updateCargo(id, status);
      await load();
    } catch (error) {
      console.error('Could not update cargo:', error);
    }
  };

  const stats = data.stats;
  const liveCount = data.live.cargo.length + data.live.personnel.length;
  const averageStock = data.inventory.length
    ? Math.round(
        data.inventory.reduce((sum, item) => {
          // Inventory has quantity and min_quantity, but no max-stock field.
          // Show a measured low-stock count instead of inventing a percentage.
          return sum + (Number(item.quantity) <= Number(item.min_quantity) ? 1 : 0);
        }, 0) / data.inventory.length * 100,
      )
    : null;

  if (loading) {
    return (
      <section className="dashboardLoading" aria-live="polite">
        <div className="loadingSpinner" />
        <h2>Loading Expedition Control Center...</h2>
      </section>
    );
  }

  return (
    <section className="dashboardPage">
      <div className="dashboardIntro">
        <div>
          <div className="dashboardEyebrow">HIMALAYAN RESEARCH · SECTOR 4</div>
          <h2>Expedition Overview</h2>
          <p>Centralized monitoring of expedition operations, cargo, personnel and resources.</p>
        </div>
        <div className="dashboardLive">
          <span className="livePulse" /> SYSTEM LIVE
        </div>
      </div>

      <div className="stats dashboardStats">
        <StatCard label="Personnel in field" value={stats.active_personnel ?? 0} icon={<Users />} detail="Active mission members" />
        <StatCard label="Cargo units tracked" value={stats.cargo_in_transit ?? 0} icon={<Package />} detail="Shipments in transit" />
        <StatCard label="Inventory items" value={data.inventory.length} icon={<Boxes />} detail={averageStock === null ? 'Resource records' : `${stats.low_stock_items ?? 0} require resupply`} />
        <StatCard label="Active alerts" value={stats.open_alerts ?? data.alerts.length} icon={<TriangleAlert />} detail="Requires attention" />
      </div>

      <div className="grid2 dashboardMainGrid">
        <section className="panel mapPanel dashboardMapPanel">
          <div className="panelHead">
            <div>
              <h2>LIVE MAP — SECTOR 4</h2>
              <small>Real-time personnel and cargo locations</small>
            </div>
            <div className="mapHeadRight">
              <small className="mapUpdated">{lastUpdated ? `updated ${lastUpdated.toLocaleTimeString()}` : 'waiting for data'}</small>
              <button className="textBtn" onClick={() => setPage('map')}>Full map →</button>
            </div>
          </div>
          <div className="mapHolder dashboardMapHolder">
            <LiveMap live={data.live} />
            <div className="dashboardMapLegend">
              <span><i className="legendCargo" /> Cargo</span>
              <span><i className="legendPersonnel" /> Personnel</span>
              <span><i className="legendAlert" /> Attention</span>
            </div>
          </div>
          <div className="mapFooter">
            <span><i className="livePulse" /> {liveCount} live locations</span>
            <button className="textBtn" onClick={() => setPage('map')}>Open live map →</button>
          </div>
        </section>

        <AlertPanel alerts={data.alerts} onResolve={resolve} />
      </div>

      <div className="grid2 dashboardBottomGrid">
        <CargoTable cargo={data.cargo} onStatus={updateCargo} />
        <InventoryPanel items={data.inventory} />
      </div>
    </section>
  );
}
