class InventoryUploadsController < ApplicationController
  def create
    batch_id = SecureRandom.uuid
    inventory_params.each do |unit|
      InventoryUnit.create(
        name: unit['name'],
        quantity: unit['quantity'].to_i,
        price: unit['price'].to_f,
        batch_id: batch_id
      )
    end
    render json: { message: 'Inventory uploaded', batch_id: batch_id }
  end

  def index
    batches = InventoryUnit.all.group_by(&:batch_id)
    result = batches.map do |batch_id, units|
      {
        batch_id: batch_id,
        number_of_units: units.count,
        average_price: (units.map(&:price).sum / units.count).round(2),
        total_quantity: units.map(&:quantity).sum
      }
    end
    render json: result
  end

  private

  def inventory_params
    params.require(:_json)
  end
end
