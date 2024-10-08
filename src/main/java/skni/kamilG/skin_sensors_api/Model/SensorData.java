package skni.kamilG.skin_sensors_api.Model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import lombok.*;

@NoArgsConstructor
@AllArgsConstructor
@ToString
@Getter
@Setter
@Entity
@Table(name = "sensor_data")
public class SensorData {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "data_id")
  private Long dataId;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "sensor_id", nullable = false)
  private Sensor sensor;

  private LocalDateTime timestamp;

  private short temperature;

  private long humidity;

  private long pressure;

  @Column(name = "gas_resistance", nullable = false)
  private long gasResistance;
}
